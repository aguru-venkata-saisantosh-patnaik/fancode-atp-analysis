"""Preserve public source responses and an auditable collection manifest.

Run from the repository root: python scripts/collect_sources.py
Existing source IDs are not fetched again unless --refresh is provided.
No authentication, certificate bypass or access-control workaround is used.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

def now():
    return datetime.now(timezone.utc).isoformat()

def collect(source):
    started = now()
    with tempfile.TemporaryDirectory() as td:
        payload = Path(td) / 'body'
        headers = Path(td) / 'headers'
        command = ['curl', '--silent', '--show-error', '--location', '--max-time', '45',
                   '--connect-timeout', '15', '--max-filesize', '80000000',
                   '--dump-header', str(headers), '--output', str(payload),
                   '--write-out', '%{http_code}\n%{url_effective}\n%{content_type}', source['url']]
        run = subprocess.run(command, capture_output=True, text=True)
        parts = run.stdout.splitlines()
        code = parts[0] if parts else '000'
        data = payload.read_bytes() if payload.exists() else b''
        content_type = parts[2] if len(parts) > 2 else ''
        successful = run.returncode == 0 and code.startswith('2') and bool(data)
        blocked_marker = any(x in data[:150000].lower() for x in [b'cf-chl-', b'just a moment...', b'access denied', b'captcha-delivery'])
        status = 'retrieved_unvalidated' if successful and not blocked_marker else 'retrieval_failed'
        digest = hashlib.sha256(data).hexdigest() if data else None
        extension = source.get('extension') or ('pdf' if data.startswith(b'%PDF') else 'json' if 'json' in content_type else 'html')
        folder = ROOT / 'data' / 'raw' / source['category']
        if status == 'retrieval_failed':
            folder = ROOT / 'data' / 'raw' / '_failed_requests' / source['category']
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / (source['id'] + '__' + (digest[:12] if digest else 'empty') + '.' + extension)
        if data and not path.exists():
            path.write_bytes(data)
        metadata = {**source, 'retrieved_at_utc': started, 'completed_at_utc': now(),
                    'http_status': code, 'final_url': parts[1] if len(parts)>1 else source['url'],
                    'content_type': content_type, 'curl_exit_code': run.returncode,
                    'bytes': len(data), 'sha256': digest, 'retrieval_status': status,
                    'file': str(path.relative_to(ROOT)) if data else None,
                    'error': run.stderr.strip()[:500] if run.stderr else None,
                    'collection_method': 'Direct unauthenticated HTTP GET via curl',
                    'content_validation': 'pending',
                    'redistribution': source.get('redistribution', 'Not established. Local research snapshot only.')}
        # Only non-sensitive response metadata is retained. No cookies or auth headers.
        return metadata

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh', action='store_true')
    parser.add_argument('--only', nargs='*')
    args = parser.parse_args()
    seeds = json.loads((ROOT/'config'/'sources.json').read_text())
    logfile = ROOT/'data'/'manifests'/'collection_log.jsonl'
    old = [json.loads(x) for x in logfile.read_text().splitlines()] if logfile.exists() else []
    attempted = {r['id'] for r in old}
    todo = [s for s in seeds if (args.refresh or s['id'] not in attempted) and (not args.only or s['id'] in args.only)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(collect, todo):
            with logfile.open('a') as file:
                file.write(json.dumps(result, ensure_ascii=False)+'\n')
            print(result['id'], result['http_status'], result['bytes'], result['retrieval_status'], flush=True)
    records = [json.loads(x) for x in logfile.read_text().splitlines()] if logfile.exists() else []
    latest = {r['id']: r for r in records}
    (ROOT/'data'/'manifests'/'sources.json').write_text(json.dumps(list(latest.values()),indent=2,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    main()
