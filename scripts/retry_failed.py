"""Bounded sequential retry of chosen source IDs, stopping a host on rate limit."""
import argparse,json,time
from pathlib import Path
from urllib.parse import urlsplit
from collect_sources import collect,ROOT

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('ids',nargs='+');p.add_argument('--delay',type=float,default=8);a=p.parse_args()
 sources={s['id']:s for s in json.loads((ROOT/'config/sources.json').read_text())}
 stopped=set();log=ROOT/'data/manifests/collection_log.jsonl'
 for i in a.ids:
  source=sources[i];host=urlsplit(source['url']).netloc
  if host in stopped:print(i,'deferred after rate limit',flush=True);continue
  result=collect(source);result['retry_round']='raw-v2'
  with log.open('a') as f:f.write(json.dumps(result,ensure_ascii=False)+'\n')
  print(i,result['http_status'],result['bytes'],flush=True)
  if result['http_status']=='429':stopped.add(host)
  time.sleep(a.delay)
 latest={r['id']:r for r in (json.loads(line) for line in log.read_text().splitlines())}
 (ROOT/'data/manifests/sources.json').write_text(json.dumps(list(latest.values()),indent=2,ensure_ascii=False)+'\n')
