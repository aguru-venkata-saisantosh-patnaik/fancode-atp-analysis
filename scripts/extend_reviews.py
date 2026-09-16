"""Resume preserved public review pagination to the registered date boundary.
No review text or identifiers are printed. Original responses remain immutable.
"""
import json, time
from datetime import datetime
import collect_reviews as capture
from google_play_scraper.features.reviews import _ContinuationToken
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs
from google_play_scraper import reviews, Sort

def parse(path):
    match=json.loads(Regex.REVIEWS.findall(path.read_text())[0])
    data=json.loads(match[0][2])
    token=data[-2][-1] if len(data)>1 and data[-2] else None
    items=data[0] if data and data[0] else []
    return [{k:s.extract_content(r) for k,s in ElementSpecs.Review.items()} for r in items],token

if __name__=='__main__':
    app='com.dream11sportsguru'
    logs=[json.loads(x) for x in capture.MANIFEST.read_text().splitlines()]
    own=[x for x in logs if x['app_id']==app and str(x['http_status']).startswith('2')]
    capture.active_app=app
    capture.batch_number=max(int(x['id'].rsplit('_',1)[1]) for x in logs)
    rows=[]
    for log in own:
        page,token=parse(capture.ROOT/log['file']);rows.extend(page)
    if any(r.get('at') and r['at'] < datetime(2025,1,1) for r in rows):
        print('Registered boundary already reached. No new request needed.')
        raise SystemExit(0)
    continuation=_ContinuationToken(token,'en','in',Sort.NEWEST.value,200,None,None)
    reason='cap_reached'; error=None
    try:
        while len(rows)<30000:
            page,continuation=reviews(app,continuation_token=continuation)
            rows.extend(page)
            dates=[r['at'] for r in page if r.get('at')]
            print('mobile',len(rows),'oldest',min(dates).isoformat() if dates else None,flush=True)
            if dates and min(dates)<datetime(2025,1,1):reason='requested_window_boundary_reached';break
            if not page or not getattr(continuation,'token',None):
                last=json.loads(capture.MANIFEST.read_text().splitlines()[-1])
                reason='source_exhausted' if str(last['http_status']).startswith('2') else 'request_failed'
                break
            time.sleep(1)
    except Exception as e:reason='request_or_parser_failed';error=str(e)
    dates=[r['at'] for r in rows if r.get('at')]
    p=capture.ROOT/'data/manifests/review_coverage.json'
    summary=json.loads(p.read_text())
    previous=next(x for x in summary if x['app_id']==app)
    (capture.ROOT/'data/manifests/review_coverage_initial.json').write_text(json.dumps(summary,indent=2)+'\n')
    new=dict(app_id=app,parsed_review_count=len(rows),unique_review_ids=len({r['reviewId'] for r in rows}),oldest=min(dates).isoformat(),newest=max(dates).isoformat(),stop_reason=reason,error=error,previous_stop_reason=previous['stop_reason'],note='Resumed from saved public pagination. Boundary batches and any post-cutoff records retained raw. Later notebook must deduplicate and filter to registered window. India storefront does not establish reviewer residence.')
    p.write_text(json.dumps([new if x['app_id']==app else x for x in summary],indent=2)+'\n')
    print(json.dumps(new,indent=2))
