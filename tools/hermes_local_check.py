"""Operator-invoked AIProFreelancer checks, callable by the existing Hermes launcher.
No model calls, generation, publishing, scheduling or purchases.
"""
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import sys
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    results = []
    def run(name, command):
        p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=180)
        results.append({'check': name, 'exit_code': p.returncode,
                        'output': p.stdout + p.stderr})
        return p
    before = run('git_status_before', ['git', '--no-optional-locks', 'status', '--porcelain=v1'])
    run('head', ['git', '--no-optional-locks', 'rev-parse', 'HEAD'])
    for pattern in ['test_content_preflight.py', 'test_publication_inventory_json.py', 'test_affiliate_audit.py', 'test_cover_assets.py', 'test_draft_quality.py']:
        result = run(pattern, [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern])
        match = re.search(r'Ran (\d+) tests?', result.stdout + result.stderr)
        if not match or int(match.group(1)) == 0:
            results[-1]['exit_code'] = 1
            results[-1]['output'] += '\nNo executed tests; review required.'
    run('reviewed_cover_references', [sys.executable, '-B', 'tools/cover_assets.py', str(ROOT)])
    run('daily_report', [sys.executable, '-B', 'tools/daily_status.py'])
    run('hypothetical_revenue_scenarios', [sys.executable, '-B', 'tools/revenue_model.py'])
    after = run('git_status_after', ['git', '--no-optional-locks', 'status', '--porcelain=v1'])
    unchanged = before.returncode == after.returncode == 0 and before.stdout == after.stdout
    report = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'repo': str(ROOT), 'result': 'PASS' if unchanged and all(r['exit_code']==0 for r in results) else 'REVIEW_REQUIRED',
              'git_status_unchanged': unchanged, 'llm_calls': 0, 'publication_attempted': False,
              'schedule_created': False, 'scope': 'Local checks only; not live tracking or revenue proof', 'checks': results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'result':report['result'],'report':str(args.output),'llm_calls':0}))
    return 0 if report['result']=='PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
