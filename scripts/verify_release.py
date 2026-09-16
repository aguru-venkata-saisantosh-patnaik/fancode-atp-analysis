"""Verify the frozen raw release using only Python's standard library."""
from pathlib import Path
import hashlib
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',help='Archived release ID under data/releases')
    args=parser.parse_args()
    base=ROOT/'data/releases'/args.archive if args.archive else ROOT
    release=json.loads((base/'data/manifests/release.json').read_text())
    checksum_path=base/release['checksum_file']
    errors=[]
    if hashlib.sha256(checksum_path.read_bytes()).hexdigest()!=release['checksum_file_sha256']:
        errors.append('Checksum-list hash differs from release lock')
    expected=set()
    for line in checksum_path.read_text().splitlines():
        digest,relative=line.split('  ',1)
        expected.add(relative)
        path=ROOT/relative
        if not path.is_file():errors.append('Missing: '+relative)
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=digest:errors.append('Changed: '+relative)
    actual={str(p.relative_to(ROOT)) for p in (ROOT/'data/raw').rglob('*') if p.is_file() and p.name!='README.md'}
    if not args.archive:
        for relative in sorted(actual-expected):errors.append('Unregistered raw file: '+relative)
    for relative,digest in release['provenance_sha256'].items():
        path=base/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            errors.append('Provenance changed: '+relative)
    print(json.dumps(dict(release_id=release['release_id'],status='FAIL' if errors else 'PASS',raw_files_checked=len(expected),errors=errors),indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
