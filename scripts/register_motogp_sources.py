"""Register public MotoGP session URLs from preserved season/category/event responses.

Only registers URLs, never downloads or transforms provider data. Excludes tests.
Endpoint parameter syntax is documented in the preserved public importer source.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 sources={x['id']:x for x in json.loads((R/'data/manifests/sources.json').read_text())}
 def body(i):return json.loads((R/sources[i]['file']).read_text())
 category=next(x for x in body('v4_motogp_categories') if x['legacy_id']==3)
 events=body('v4_motogp_finished_events')+body('v4_motogp_future_events')
 events={x['id']:x for x in events if not x['test'] and x['season']['year']==2026}
 p=R/'config/sources.json';seeds=json.loads(p.read_text());known={x['id'] for x in seeds};count=0
 for e in events.values():
  sid='v4_motogp_sessions_'+e['short_name'].lower()
  if sid in known:continue
  seeds.append(dict(id=sid,category='schedules',extension='json',url='https://api.motogp.pulselive.com/motogp/v1/results/sessions?eventUuid='+e['id']+'&categoryUuid='+category['id'],purpose='Official public MotoGP-class session records for '+e['name']+'. Date/time semantics require validation.',registration_parents=['v4_motogp_categories','v4_motogp_finished_events','v4_motogp_future_events','v4_motogp_sessions_code']))
  count+=1
 p.write_text(json.dumps(seeds,indent=2,ensure_ascii=False)+'\n');print('Registered',count,'session sources')
if __name__=='__main__':main()
