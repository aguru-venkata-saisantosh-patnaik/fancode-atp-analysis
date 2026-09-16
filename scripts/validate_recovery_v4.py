"""Offline raw-v4 source QA. Counts coverage and tests evidence semantics, not business outcomes."""
import csv,hashlib,json,re
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
def main():
 sources={x['id']:x for x in json.loads((R/'data/manifests/sources.json').read_text())}
 new={k:v for k,v in sources.items() if k.startswith('v4_')}
 for src in new.values():
  if src['file']:assert hashlib.sha256((R/src['file']).read_bytes()).hexdigest()==src['sha256']
 def path(i):return R/sources[i]['file']
 def body(i):return json.loads(path(i).read_text())
 def txt(i):return BeautifulSoup(path(i).read_text(),'html.parser').get_text(' ',strip=True)
 def anti_json(i):
  t=path(i).read_text();return json.loads(t[t.index('{'):])
 football=[]
 for sid,expected in [('v4_laliga_2526',380),('v4_laliga_2627',41)]:
  rows=list(csv.DictReader(path(sid).open(encoding='utf-8-sig')))
  assert len(rows)==expected
  assert len({(x['Date'],x['HomeTeam'],x['AwayTeam']) for x in rows})==len(rows)
  dates=[datetime.strptime(x['Date']+' '+x['Time'],'%d/%m/%Y %H:%M') for x in rows]
  football.append(dict(source_id=sid,rows=len(rows),first_date=min(dates).isoformat(),last_date=max(dates).isoformat(),in_2026_through_sep12=sum(datetime(2026,1,1)<=d<datetime(2026,9,13) for d in dates),after_sep12=sum(d>=datetime(2026,9,13) for d in dates),all_clocks_parse=True,timezone_status='Europe/London inference supported by two primary fixture checks and independent integration documentation. Provider notes do not state timezone.'))
  if sid=='v4_laliga_2526':
   winter=next(x for x in rows if x['Date']=='03/01/2026' and x['AwayTeam']=='Barcelona')
   summer=next(x for x in rows if x['Date']=='10/05/2026' and x['AwayTeam']=='Real Madrid')
   assert winter['Time']==summer['Time']=='20:00'
   for d in ['2026-01-03T20:00:00','2026-05-10T20:00:00']:
    assert datetime.fromisoformat(d).replace(tzinfo=ZoneInfo('Europe/London')).astimezone(ZoneInfo('Europe/Madrid')).hour==21
 assert '9pm CET' in txt('v4_barca_winter_time')
 assert '9:00 pm CEST' in txt('v4_madrid_summer_time')
 assert 'UK time' in txt('v4_football_tz_documentation')
 events=body('v4_motogp_finished_events')+body('v4_motogp_future_events')
 events={e['id']:e for e in events if not e['test'] and e['season']['year']==2026}
 assert len(events)==22
 sessions=[];per_event=[]
 for sid,src in new.items():
  if not sid.startswith('v4_motogp_sessions_') or src.get('extension')!='json':continue
  rows=body(sid);assert rows
  assert len({x['id'] for x in rows})==len(rows)
  assert all(x['event']['id'] in events and x['category']['legacy_id']==3 for x in rows)
  assert all(datetime.fromisoformat(x['date']).tzinfo for x in rows)
  sessions+=rows
  per_event.append(dict(source_id=sid,event=rows[0]['event']['short_name'],records=len(rows),race_records=sum(x['type']=='RAC' for x in rows),statuses=dict(Counter(x['status'] for x in rows))))
 assert len(per_event)==22
 assert len({x['id'] for x in sessions})==len(sessions)
 ned=next(x for x in body('v4_motogp_sessions_ned') if x['type']=='RAC')
 assert ned['date']=='2026-06-28T14:00:00+00:00'
 timetable=PdfReader(path('v4_assen_timetable')).pages[0].extract_text()
 assert 'UTC +2 hours' in timetable and '14:00 MotoGP' in timetable
 assert '14:00' in txt('v4_motogp_assen_official')
 reports=[]
 for sid,src in new.items():
  if not sid.startswith('v4_motogp_report_'):continue
  pdf=PdfReader(path(sid));page_hits=[]
  for i,page in enumerate(pdf.pages[:3]):
   text=page.extract_text() or ''
   clocks=re.findall(r'RACE START\s+(\d{1,2}:\d{2}[\'’]\d{2})',text)
   if clocks:page_hits.append(dict(page=i+1,race_start_clocks=list(dict.fromkeys(clocks))))
  reports.append(dict(source_id=sid,pages=len(pdf.pages),pages_scanned=min(3,len(pdf.pages)),race_start_evidence=page_hits,semantics='Race-control local clock. May repeat history across documents and include restarts. No blanket UTC conversion.'))
 assert len(reports)==29 and all(x['race_start_evidence'] for x in reports)
 ned_report=next(x for x in reports if x['source_id']=='v4_motogp_report_ned_rac')
 assert any("14:02'03" in p['race_start_clocks'] for p in ned_report['race_start_evidence'])
 cat=next(x for x in reports if x['source_id']=='v4_motogp_report_cat_rac2')
 assert len({t for p in cat['race_start_evidence'] for t in p['race_start_clocks']})>=3
 explore=anti_json('v4_trends_2025_pair');ts=anti_json('v4_trends_2025_timeline')['default']['timelineData']
 assert len(ts)==53 and all(len(x['value'])==2 for x in ts)
 assert all(0<=v<=100 for x in ts for v in x['value'])
 assert len({x['time'] for x in ts})==53
 assert '2024' in ts[0]['formattedTime'] and '2026' in ts[-1]['formattedTime']
 assert sources['v4_trends_football_pair']['http_status']=='429'
 affiliate=txt('v4_sonyliv_affiliate')
 assert all(x in affiliate for x in ['234.00','135.00','paused by the advertiser'])
 assert 'merchandise' in txt('v4_xpert_fancode').lower()
 assert 'COD' in txt('v4_gokwik_fancode')
 assert 'Fancode Shop' in txt('v4_fancode_shop_affiliate')
 assert all(x in txt('v4_mint_isl_audience') for x in ['5.79 million','9.39 million','AIFF document'])
 assert '23 tournament weeks' in txt('v4_deltatre_fantasy')
 assert all(x in txt('v4_jio_ott_delivery') for x in ['FanCode','JioTV mobile app'])
 assert all(x in txt('v4_vi_ott_web') for x in ['199 per month','248 per month','auto renew every month'])
 result=dict(author='Competition team',checked_at_utc=datetime.now(timezone.utc).isoformat(),result='PASS',new_http_sources=len(new),retrieved=sum(x['retrieval_status']=='retrieved_unvalidated' for x in new.values()),failed=sum(x['retrieval_status']=='retrieval_failed' for x in new.values()),football=football,motogp=dict(events=22,session_records=len(sessions),session_types=dict(Counter(x['type'] for x in sessions)),status_counts=dict(Counter(x['status'] for x in sessions)),raw_dates_after_sep12=sum(x['date'][:10]>'2026-09-12' for x in sessions),per_event=per_event,official_reports=reports,timezone_defect='Assen API literal +00:00 and ICS Z conflict with official local UTC+2 schedule. Quarantine offsets until per-circuit normalization is justified. API records are not an actual-start log.'),trends=dict(rows=53,series=['tennis','FanCode'],geo='IN',requested_window='2025-01-01 2025-12-31',frequency='weekly',first_bin=ts[0]['formattedTime'],last_bin=ts[-1]['formattedTime'],boundary_warning='First and last weekly bins cross requested year boundaries. Do not prorate weekly values or compare levels against separately normalized 2026 data.',football_status='HTTP 429, not recovered'),visual_checks=['Assen race report page 2: race start 14:02:03','Catalunya RAC2 report page 2: race starts 14:02:17 and 14:53:06 with intervening red flags'],scope='PASS is source integrity and explicit data-defect detection, not evidence that all source values are correct or complete.')
 (R/'data/manifests/recovery_v4_qa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:result[k] for k in ['result','new_http_sources','retrieved','failed']}));print('football',football);print('MotoGP',len(sessions),'sessions,',len(reports),'reports');print('Trends',len(ts),'weekly rows')
if __name__=='__main__':main()
