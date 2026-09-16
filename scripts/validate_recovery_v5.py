"""Offline checks for recovered football data and complete failure dispositions."""
from pathlib import Path
import json,csv,io,hashlib
from datetime import datetime,timedelta
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1];M=R/'data/manifests'
s=json.loads((M/'sources.json').read_text());by={x['id']:x for x in s}
c=json.loads((M/'manual_captures.json').read_text());cap={x['id']:x for x in c}
r=cap['google_trends_football_table_v5'];b=(R/r['file']).read_bytes();t=b.decode();assert len(t)==4343 and hashlib.sha256(b).hexdigest()==r['sha256']
h=2166136261
for ch in t:h=((h^ord(ch))*16777619)&0xffffffff
assert f'{h:08x}'=='6705d050'
rows=list(csv.reader(io.StringIO(t),delimiter='\t'));assert rows[0]==['x','y1','y2'] and len(rows)==256
for i,row in enumerate(rows[1:]):
 assert len(row)==3 and datetime.strptime(row[0],'%b %d, %Y')==datetime(2026,1,1)+timedelta(days=i)
 assert all(0<=int(x)<=100 for x in row[1:])
d=json.loads((M/'failure_disposition.json').read_text());failed={x['id'] for x in s if x['retrieval_status']=='retrieval_failed'}
assert len(d['items'])==len(failed)==d['failed_source_count']
assert {x['source_id'] for x in d['items']}==failed
for x in d['items']:
 assert x['disposition'] and x['replacement_ids']
 assert all(i in by or i in cap for i in x['replacement_ids'])
 assert all(i not in failed for i in x['replacement_ids'])
g=PdfReader(R/by['v5_gst_council_rates']['file']);assert '9984' in g.pages[32].extract_text()
a=PdfReader(R/by['v5_atp_media_guide_lta']['file']);assert len(a.pages)==160
assert '2026 ATP Tour season' in a.pages[2].extract_text() and 'BRISBANE' in a.pages[14].extract_text()
result=dict(result='PASS',football_rows=255,football_fnv1a='6705d050',failed_sources_dispositioned=len(failed),atp_guide_pages=160,gst_rate_table_pdf_page=33,limitations='Checks prove preserved table continuity, provenance coverage and selected document identity. They do not prove causal validity, complete season coverage or entitlement.')
(M/'recovery_v5_qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
