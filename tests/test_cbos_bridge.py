import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, 'D:/CBOS')
sys.path.insert(0, 'D:/CBOS/tests')
from cbos_bridge import BridgeError, stage, import_draft, publish
from core.kernel.review_export import export_review_bundle
import test_review_bundle as fixtures


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        factory = fixtures.ReviewBundleTest()
        factory.setUp()
        self.addCleanup(factory.tearDown)
        self.bundle = factory.bundle()
        self.factory = factory
        self.source = export_review_bundle(self.bundle, self.root)
        self.site = self.root / 'site'
        self.site.mkdir()
        (self.site / 'hugo.toml').write_text('baseURL="https://example.com"')
        self.addCleanup(self.temp.cleanup)

    def prepare(self):
        return stage(self.source, 'D:/CBOS', self.root, 'fixture-article', True)

    def test_stage_real_bundle_and_rewrite_images(self):
        package, checksum = self.prepare()
        article = (package / 'content/posts/fixture-article.md').read_text(encoding='utf-8')
        front, _ = json.JSONDecoder().raw_decode(article)
        self.assertTrue(front['draft'])
        self.assertIn('(/images/cbos/', article)
        self.assertEqual(hashlib.sha256((package/'receipt.json').read_bytes()).hexdigest(), checksum)

    def test_fixture_never_imported(self):
        package, checksum = self.prepare()
        with self.assertRaises(BridgeError):
            import_draft(package, self.site, checksum)
        self.assertFalse((self.site / 'content').exists())

    def test_fixture_opt_in(self):
        with self.assertRaises(BridgeError):
            stage(self.source, 'D:/CBOS', self.root, 'fixture-article')

    def test_tampered_article_rejected(self):
        (self.source / 'article.md').write_text('Invented facts')
        with self.assertRaises(BridgeError):
            self.prepare()

    def test_tampered_image_rejected(self):
        image = next((self.source / 'assets').iterdir())
        image.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            self.prepare()

    def test_traversal_rejected(self):
        with self.assertRaises(BridgeError):
            stage(self.source, 'D:/CBOS', self.root, '../escape', True)

    def test_no_overwrite(self):
        self.prepare()
        with self.assertRaises(FileExistsError):
            self.prepare()

    def test_approval_hash_required(self):
        package, _ = self.prepare()
        with self.assertRaises(BridgeError):
            import_draft(package, self.site, '0' * 64)

    def test_extra_bundle_file_rejected(self):
        (self.source / 'extra.txt').write_text('unexpected')
        with self.assertRaises(BridgeError):
            self.prepare()

    def test_import_nonfixture_schema_and_duplicate_block(self):
        # Synthetic source, nonfixture flag only to exercise the import boundary.
        nonfixture = self.factory.bundle(fixture=False)
        source = export_review_bundle(nonfixture, self.root)
        package, checksum = stage(source, 'D:/CBOS', self.root, 'import-test')
        result = import_draft(package, self.site, checksum)
        self.assertEqual(result['state'], 'IMPORTED_DRAFT')
        self.assertFalse(result['published'])
        with self.assertRaises(BridgeError):
            import_draft(package, self.site, checksum)

    def test_changed_package_fails_before_writing(self):
        source = export_review_bundle(self.factory.bundle(fixture=False), self.root)
        package, checksum = stage(source, 'D:/CBOS', self.root, 'changed-test')
        (package / 'content/posts/changed-test.md').write_text('tampered')
        with self.assertRaises(BridgeError):
            import_draft(package, self.site, checksum)
        self.assertFalse((self.site / 'content').exists())

    def publication_setup(self):
        source = export_review_bundle(self.factory.bundle(fixture=False), self.root)
        package, checksum = stage(source, 'D:/CBOS', self.root, 'publish-test')
        remote = self.root / 'remote.git'
        def git(*args, cwd=self.site):
            subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True)
        git('init', '--bare', str(remote), cwd=self.root)
        git('init', '-b', 'main')
        git('config', 'user.name', 'Offline Test')
        git('config', 'user.email', 'test@example.com')
        git('add', 'hugo.toml')
        git('commit', '-m', 'fixture baseline')
        git('remote', 'add', 'origin', str(remote))
        git('push', 'origin', 'main')
        import_draft(package, self.site, checksum)
        journal = self.root / 'journal'
        journal.mkdir()
        return package, checksum, journal, remote

    def test_publish_exact_files_to_local_bare_remote(self):
        package, checksum, journal, remote = self.publication_setup()
        (self.site / 'unrelated.txt').write_text('must not enter Git')
        actual_run = subprocess.run
        def run(args, **kwargs):
            if args[0] == 'hugo':
                return subprocess.CompletedProcess(args, 0, '', '')
            return actual_run(args, **kwargs)
        with patch('cbos_bridge.subprocess.run', side_effect=run):
            result = publish(package, self.site, checksum, journal)
        self.assertEqual(result['state'], 'PUSHED_DEPLOY_PENDING')
        tracked = subprocess.run(['git', 'ls-tree', '-r', '--name-only', 'main'],
                                 cwd=remote, capture_output=True, text=True, check=True).stdout
        self.assertNotIn('unrelated.txt', tracked)
        self.assertIn('content/posts/publish-test.md', tracked)
        article = (self.site / 'content/posts/publish-test.md').read_text(encoding='utf-8')
        self.assertFalse(json.JSONDecoder().raw_decode(article)[0]['draft'])

    def test_daily_reservation_blocks_second_article(self):
        package, checksum, journal, _ = self.publication_setup()
        actual_run = subprocess.run
        def run(args, **kwargs):
            if args[0] == 'hugo':
                return subprocess.CompletedProcess(args, 0, '', '')
            return actual_run(args, **kwargs)
        with patch('cbos_bridge.subprocess.run', side_effect=run):
            publish(package, self.site, checksum, journal)
            source = self.root / json.loads((package / 'receipt.json').read_text())['bundle_id']
            second, approval = stage(source, 'D:/CBOS', self.root, 'second-test')
            import_draft(second, self.site, approval)
            with self.assertRaises(FileExistsError):
                publish(second, self.site, approval, journal)
        front, _ = json.JSONDecoder().raw_decode((self.site / 'content/posts/second-test.md').read_text(encoding='utf-8'))
        self.assertTrue(front['draft'])

    def test_partial_bundle_never_staged(self):
        partial = self.factory.bundle(images=())
        source = export_review_bundle(partial, self.root)
        with self.assertRaises(BridgeError):
            stage(source, 'D:/CBOS', self.root, 'partial-test', True)

    def test_unrelated_staged_work_blocks_publication(self):
        package, checksum, journal, _ = self.publication_setup()
        (self.site / 'unrelated.txt').write_text('preserve')
        subprocess.run(['git', 'add', 'unrelated.txt'], cwd=self.site, check=True, capture_output=True)
        with self.assertRaises(BridgeError):
            publish(package, self.site, checksum, journal)
        self.assertEqual(list(journal.iterdir()), [])

    def test_lost_push_response_remains_unknown(self):
        package, checksum, journal, _ = self.publication_setup()
        actual_run = subprocess.run
        def run(args, **kwargs):
            if args[0] == 'hugo':
                return subprocess.CompletedProcess(args, 0, '', '')
            if args[:2] == ['git', 'push']:
                raise subprocess.TimeoutExpired(args, 120)
            return actual_run(args, **kwargs)
        with patch('cbos_bridge.subprocess.run', side_effect=run), self.assertRaises(subprocess.TimeoutExpired):
            publish(package, self.site, checksum, journal)
        self.assertEqual(json.loads(next(journal.iterdir()).read_text())['state'], 'UNKNOWN_REQUIRES_INSPECTION')
