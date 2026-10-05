"""Read-only operator report. Repository facts are not live traffic/revenue proof."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from content_preflight import inventory


def report(root, today):
    posts = root / 'content' / 'posts'
    state = inventory(posts, today)
    lines = [f'# AIProFreelancer — kiểm tra ngày {today}', '',
             'Nguồn: repo hiện tại; không thay thế biên nhận live hoặc dashboard.', '',
             '## Giới hạn xuất bản website', '',
             f"Bài không phải draft mang ngày hôm nay: {len(state['published_today'])}.",
             'Đã đủ giới hạn: không đăng thêm.' if state['published_today'] else
             'Chưa có bài trong inventory hôm nay; vẫn phải kiểm tra journal và remote trước đăng.',
             *[f'- {name}' for name in sorted(state['published_today'])], '',
             '## Bản nháp trong repo', '']
    preparation_path = root / 'data' / 'prepared_drafts.json'
    prepared = json.loads(preparation_path.read_text(encoding='utf-8')) if preparation_path.exists() else {}
    for path in sorted(posts.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        if text.startswith('{'):
            fields, _ = json.JSONDecoder().raw_decode(text)
        elif text.startswith('---'):
            fields = dict(re.findall(r'^([a-z]+):\s*(.*?)\s*$', text.split('---', 2)[1], re.M))
        else:
            continue
        if str(fields.get('draft', 'false')).lower() == 'true':
            date = str(fields.get('date', '')).strip('"\'')
            record = prepared.get(path.name)
            label = 'Chưa có bản ghi chuẩn bị; cần rà soát nội dung và tài sản.'
            if record:
                files = record['files']
                matches = all((root / name).is_file() and
                              hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
                              for name, digest in files.items())
                label = ('Bản chuẩn bị và tài sản khớp ghi nhận; vẫn phải kiểm tra ngày, journal và remote.'
                         if matches else 'Đã thay đổi hoặc thiếu tài sản kể từ bản chuẩn bị; cần rà soát lại.')
            lines.append(f'- {path.name}: ngày dự kiến {date}; chưa tính live. {label}')
    lines.append('Bản ghi chuẩn bị chỉ phục vụ báo cáo, không cấp quyền hoặc tự mở draft để xuất bản.')
    lines += ['', '## Chương trình affiliate — dữ liệu lưu lần gần nhất', '']
    catalog = json.loads((root / 'data' / 'affiliate-catalog.json').read_text(encoding='utf-8'))
    for item in catalog['records']:
        captured = item['evidence']['captured_at']
        unknown = []
        if item.get('cookie_days') is None:
            unknown.append('cookie')
        if item['commission'].get('duration_months') is None:
            unknown.append('thời hạn hoa hồng')
        lines.append(f"- {item['label']}: {item['status']}; đọc lần cuối {captured}; "
                     f"cần xác minh: {', '.join(unknown) or 'điều khoản và hiệu lực hiện tại'}.")
    audience_path = root / 'data' / 'audience-pilot.json'
    if audience_path.exists():
        pilot = json.loads(audience_path.read_text(encoding='utf-8'))
        program_ids = {item['program_id'] for item in catalog['records']}
        lines += ['', '## Nhóm khách hàng pilot — giả thuyết cần kiểm chứng', '',
                  f"Dữ liệu biên tập ngày {pilot['updated_on']}; chưa chứng minh nhu cầu hoặc doanh thu."]
        for segment in pilot['segments']:
            unknown_ids = set(segment['program_ids']) - program_ids
            if unknown_ids:
                raise ValueError(f"Unknown program IDs in {segment['id']}: {sorted(unknown_ids)}")
            lines += [f"- {segment['id']}: {segment['audience']}",
                      f"  Trang vào: {segment['entry_page']}; chương trình: {', '.join(segment['program_ids'])}.",
                      f"  Điều kiện mua cần kiểm tra: {segment['purchase_gate']}",
                      f"  Bằng chứng còn cần: {', '.join(segment['validation_needed'])}."]
            if segment.get('top_traffic_countries') is None:
                lines.append('  Top quốc gia traffic: chưa có dữ liệu phù hợp, không suy ra từ market keyword.')
    geography_path = root / 'data' / 'market-geography.json'
    if geography_path.exists():
        geography = json.loads(geography_path.read_text(encoding='utf-8'))
        lines += ['', '## Gợi ý thị trường — traffic nhà cung cấp, không phải khách mua', '',
                  f"Similarweb ước tính kỳ {geography['displayed_period']}, đọc ngày {geography['captured_on']}.",
                  geography['traffic_scope_note']]
        for record in geography['records']:
            if record['program_id'] not in {item['program_id'] for item in catalog['records']}:
                raise ValueError(f"Unknown geography program: {record['program_id']}")
            countries = ', '.join(f"{c['country']} {c['share']:.2f}%" for c in record['countries'])
            lines.append(f"- {record['domain']}: {countries}. Nguồn: {record['source_url']}")
        lines.append(geography['decision'])
    lines += ['', '## Kiểm tra bằng dữ liệu thực', '',
              '- Fanpage: đọc lịch sử trước khi đăng; tối đa 1/ngày, 3/tuần.',
              '- GA: cùng cửa sổ ngày cho sessions, affiliate_click và checklist_download_click.',
              '- Dashboard offer: tách clicks, conversion được duyệt, commission và tiền nhận.',
              '- Ghi thời gian giám sát thực; mục tiêu ≤30 phút/ngày chưa được chứng minh.',
              '- Không tạo traffic hoặc conversion thử để đạt KPI.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=datetime.now(timezone(timedelta(hours=7))).date().isoformat())
    parser.add_argument('--output', type=Path, help='Save UTF-8 report; never modifies posts or publishes.')
    args = parser.parse_args()
    datetime.strptime(args.date, '%Y-%m-%d')
    result = report(Path(__file__).resolve().parents[1], args.date)
    if args.output:
        args.output.write_text(result, encoding='utf-8')
    else:
        sys.stdout.reconfigure(encoding='utf-8')
        print(result)
