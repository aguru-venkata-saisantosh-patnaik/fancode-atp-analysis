"""Register official sprint/race session-report URLs from saved public API bodies."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 sources=json.loads((R/'data/manifests/sources.json').read_text());p=R/'config/sources.json';seeds=json.loads(p.read_text());known={x['id'] for x in seeds};count=0
 for src in sources:
  if not src['id'].startswith('v4_motogp_sessions_') or src.get('extension')!='json' or src['retrieval_status']!='retrieved_unvalidated':continue
  for session in json.loads((R/src['file']).read_text()):
   url=session['session_files']['session']['url']
   if session['type'] not in ['SPR','RAC'] or not url:continue
   code=session['event']['short_name'].lower();kind=url.split('/')[-2].lower();sid=f'v4_motogp_report_{code}_{kind}'
   if sid in known:continue
   seeds.append(dict(id=sid,url=url,extension='pdf',category='schedules',purpose='Official session report, check reported start/end clock and race restart semantics',registration_parents=[src['id']]))
   known.add(sid);count+=1
 p.write_text(json.dumps(seeds,indent=2,ensure_ascii=False)+'\n');print('Registered',count,'official reports')
if __name__=='__main__':main()
