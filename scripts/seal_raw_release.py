"""Seal a validated local raw collection. Does not fetch or publish data."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'data/manifests'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release-id',required=True)
    args=parser.parse_args()
    previous=json.loads((M/'release.json').read_text())
    if previous['release_id']!=args.release_id and not (ROOT/'data/releases'/previous['release_id']/'data/manifests/release.json').exists():
        raise SystemExit('Archive current release metadata before replacing its lock')
    qa=json.loads((M/'validation_report.json').read_text())
    assert qa['result']=='PASS' and not qa['errors']
    assert json.loads((M/'external_evidence_qa.json').read_text())['result']=='PASS'
    assert json.loads((M/'recovery_v4_qa.json').read_text())['result']=='PASS'
    assert json.loads((M/'recovery_v5_qa.json').read_text())['result']=='PASS'
    inventory=json.loads((M/'raw_inventory.json').read_text())
    assert len(inventory)==qa['raw_files']
    sources=json.loads((M/'sources.json').read_text())
    reviews=json.loads((M/'source_validation.json').read_text())
    byid={x['source_id']:x for x in reviews}
    assert len(sources)==len(byid)==len(reviews)
    assert all(byid[x['id']]['file']==x['file'] for x in sources)
    for row in inventory:assert digest(ROOT/row['file'])==row['sha256']
    checksum=M/'RAW_SHA256SUMS.txt'
    checksum.write_text(''.join(x['sha256']+'  '+x['file']+'\n' for x in inventory))
    provenance=[M/x for x in ['collection_log.jsonl','review_collection_log.jsonl','sources.json','local_inputs.json','manual_captures.json','source_validation.json','results_source_qa.json','video_source_qa.json','external_evidence_qa.json','recovery_v4_qa.json','recovery_v5_qa.json','failure_disposition.json']]
    provenance+=list((ROOT/'config').glob('*.json'))+list((ROOT/'scripts').glob('*.py'))+list((ROOT/'docs').glob('*.md'))
    provenance+=[ROOT/'README.md',ROOT/'data/raw/README.md',ROOT/'requirements-collection.txt']
    release=dict(release_id=args.release_id,author='Competition team',sealed_at_utc=datetime.now(timezone.utc).isoformat(),status='collection_closed_with_documented_gaps',raw_files=qa['raw_files'],raw_bytes=qa['raw_bytes'],http_source_ids=qa['http_source_ids'],http_retrieved=qa['http_retrieved'],http_failed=qa['http_failed'],browser_observations=qa['browser_observations'],supplied_documents=qa['local_input_files'],unique_reviews_by_app={x['app_id']:x['unique_review_ids'] for x in qa['review_coverage']},in_window_reviews_by_app={x['app_id']:x['within_registered_window'] for x in qa['review_coverage']},integrity_result='PASS',checksum_file=str(checksum.relative_to(ROOT)),checksum_file_sha256=digest(checksum),provenance_sha256={str(p.relative_to(ROOT)):digest(p) for p in sorted(set(provenance))},availability_report='docs/DATA_AVAILABILITY.md',recovery_report='docs/RAW_V5_CLOSURE.md',previous_release=(previous['release_id'] if previous['release_id']!=args.release_id else previous.get('previous_release')),limitations=['2026 four-term daily, separate football/FanCode daily and 2025 two-term weekly Trends have different normalization','Monthly ATP inclusion and current ATP checkout price unresolved','Uneven ATP planned-time sample, no ATP actual-start census. MotoGP API offset defects and report restarts require explicit handling. Partial La Liga coverage','Secondary results date and identifier inconsistencies require reconciliation','Video keyword searches are incomplete and not India-specific','No internal cohorts, rights costs or observed channel payer conversion'],notes='All prior-release bodies retained. External vendor rates and survey estimates are separately qualified. Integrity is not proof of completeness, causal validity or redistribution permission.')
    (M/'release.json').write_text(json.dumps(release,indent=2)+'\n')
    print(json.dumps({k:release[k] for k in ['release_id','raw_files','raw_bytes','http_source_ids','integrity_result']},indent=2))
if __name__=='__main__':main()
