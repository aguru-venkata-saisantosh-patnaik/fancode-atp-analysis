"""Offline checks of raw results schemas and unsafe join/date assumptions."""
import csv,json
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'data/manifests'
def main():
    sources={x['id']:x for x in json.loads((M/'sources.json').read_text())}
    ids=['sackmann_archive_2025','sackmann_archive_2026','tennismylife_2025','tennismylife_2026','tennismylife_ongoing']
    qa=[]
    for i in ids:
        with (ROOT/sources[i]['file']).open() as f:rows=list(csv.DictReader(f))
        dates=[r['tourney_date'] for r in rows]
        keys=[(r['tourney_id'],r['match_num']) for r in rows]
        eventdates=defaultdict(set)
        for r in rows:eventdates[r['tourney_id']].add(r['tourney_date'])
        qa.append(dict(source_id=i,rows=len(rows),columns=len(rows[0]),tournament_ids=len(eventdates),min_date_field=min(dates),max_date_field=max(dates),event_ids_with_multiple_dates=sum(len(x)>1 for x in eventdates.values()),duplicate_tournament_match_keys=len(keys)-len(set(keys)),missing_match_num=sum(not r['match_num'] for r in rows),missing_minutes=sum(not r['minutes'] for r in rows),has_match_start_time=False,date_semantics='Tournament-week per source dictionary' if i.startswith('sackmann') else 'Publisher documentation says tournament week. 2026 and ongoing files vary within events, while the 2025 file does not. Check this file’s event_ids_with_multiple_dates. Date basis and timezone unresolved.',join_warning='Never discard rows solely because tournament_id plus match_num repeats. Missing numbers and reused keys exist.'))
    (M/'results_source_qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(json.dumps(qa,indent=2))
if __name__=='__main__':main()
