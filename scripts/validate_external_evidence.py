"""Offline provenance and selected source-value QA. No model estimation or network."""
import csv,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from bs4 import BeautifulSoup
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
def main():
 sources={x['id']:x for x in json.loads((R/'data/manifests/sources.json').read_text())}
 metrics=json.loads((R/'config/external_evidence_registry.json').read_text())['metrics']
 ids=[m['metric_id'] for m in metrics];assert len(ids)==len(set(ids))
 for m in metrics:
  src=sources[m['source_id']]
  assert m['source_url']==src['url'] and m['raw_file']==src['file']
  assert src['retrieval_status']=='retrieved_unvalidated'
  assert hashlib.sha256((R/src['file']).read_bytes()).hexdigest()==src['sha256']
  assert all(m.get(k) for k in ['unit','population','measurement_period','evidence_type','locator','limitations'])
 def path(i):return R/sources[i]['file']
 def htmltext(i):return BeautifulSoup(path(i).read_text(),'html.parser').get_text(' ',strip=True)
 apple=htmltext('v3_tennistv_india_iap')
 assert all(v in apple for v in ['449','2,500','4,499','MONTHLY','ANNUAL'])
 ibm=PdfReader(path('v3_ibm_sports_survey_2025')).pages[59].extract_text()
 assert 'INDIA 60% 33% 37% 22% 22% 16% 14% 8% 10% 91% 4% 7%' in ibm
 ey=PdfReader(path('v3_ficci_ey_2026')).pages[44].extract_text()
 assert all(v in ey for v in ['216 million','143 million','71%'])
 meta=PdfReader(path('v3_meta_inr_ratecard_jan2026')).pages[0].extract_text()
 assert 'India ₹ 0.8631 0.1150 0.1150 2.3000' in meta
 terms=htmltext('v3_fancode_terms');assert '1-25 25 26-75 75 76-199 150 200 and above 500' in terms
 j=json.loads(path('v3_jolpica_races_2026').read_text())['MRData'];races=j['RaceTable']['Races']
 assert int(j['total'])==len(races)==23
 assert len({r['round'] for r in races})==23
 for r in races:datetime.fromisoformat(r['date']+'T'+r['time'].replace('Z','+00:00'))
 assert any(r['date']=='2026-10-04' and r['Circuit']['Location']['country']=='Malaysia' for r in races)
 rows=list(csv.DictReader(path('v3_richautomate_dataset').open()))
 assert rows and {'provider','marketing_msg_inr','verified'}<=set(rows[0])
 # Baseline and plan variants are not distinct providers.
 report=dict(author='Competition team',checked_at_utc=datetime.now(timezone.utc).isoformat(),result='PASS',registered_metrics=len(metrics),http_additions_by_release={'v3':sum(k.startswith('v3_') for k in sources),'v4':sum(k.startswith('v4_') for k in sources),'v5':sum(k.startswith('v5_') for k in sources)},f1_rounds=len(races),vendor_csv_rows=len(rows),checks=['Metric source IDs, URLs, paths and raw hashes','Selected App Store featured prices','IBM India source table and EY page45 values','Dated Meta India ratecard and referral matrix','F1 unique rounds and parseable UTC clocks','Vendor CSV schema'],limitations=['Integrity and transcription checks are not validation of publisher estimates','No FanCode causal, willingness-to-pay or internal cohort data','Tennis Explorer timezone ambiguity remains unresolved'])
 (R/'data/manifests/external_evidence_qa.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
