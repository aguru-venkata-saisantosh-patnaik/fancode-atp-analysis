"""Capture original public Play Store review response bodies before parsing.

The parser is google-play-scraper. Its network helper is replaced with verified
curl requests. Public raw responses remain local, with reviewer metadata intact.
Only coverage counts are printed. No text cleaning or sentiment analysis occurs.
"""
import hashlib
import json
import ssl
import subprocess
import tempfile
import time
import os
os.environ["TZ"] = "Asia/Kolkata"
if hasattr(time, "tzset"): time.tzset()
from datetime import datetime, timezone
from pathlib import Path
import google_play_scraper.utils.request as transport
from google_play_scraper import reviews, Sort

# The installed parser changes Python's default SSL context on import.
# Restore verification immediately and use verified curl for all requests.
ssl._create_default_https_context = ssl.create_default_context
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT/'data/raw/reviews/google_play'
RAW.mkdir(parents=True, exist_ok=True)
MANIFEST = ROOT/'data/manifests/review_collection_log.jsonl'
active_app = ''
batch_number = 0

def secure_capture(request):
    global batch_number
    batch_number += 1
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)/'response'
        cmd=['curl','--silent','--show-error','--location','--max-time','40','--connect-timeout','15',
             '--output',str(out),'--write-out','%{http_code}',request.full_url]
        if request.data is not None:
            body=Path(td)/'request'
            body.write_bytes(request.data)
            cmd += ['--request','POST','--data-binary','@'+str(body)]
        for key,val in request.header_items():
            cmd += ['--header',key+': '+val]
        res=subprocess.run(cmd,capture_output=True,text=True)
        data=out.read_bytes() if out.exists() else b''
        digest=hashlib.sha256(data).hexdigest()
        path=RAW/f'{active_app}_response_{batch_number:03d}_{digest[:12]}.txt'
        if not path.exists(): path.write_bytes(data)
        record=dict(id=f'{active_app}_{batch_number:03d}',app_id=active_app,
            source_url=request.full_url,method='Public review RPC via verified curl, parser google-play-scraper',
            retrieved_at_utc=datetime.now(timezone.utc).isoformat(),http_status=res.stdout,
            bytes=len(data),sha256=digest,file=str(path.relative_to(ROOT)),locale='en-IN',
            requested_sort='newest',redistribution='Not established. Contains public reviewer metadata. Local snapshot only.')
        with MANIFEST.open('a') as f:f.write(json.dumps(record)+'\n')
        if res.returncode or not res.stdout.startswith('2'):
            raise RuntimeError('Public review request failed: HTTP '+res.stdout+' '+res.stderr[:150])
        return data.decode('utf-8')

transport._urlopen=secure_capture
transport.MAX_RETRIES=1

def main():
    global active_app
    summary=[]
    for app_id,cap in [('com.dream11sportsguru',30000),('com.fancode.tv',3000)]:
        active_app=app_id
        rows=[]
        continuation=None
        reason='cap_reached'
        error=None
        try:
            while len(rows)<cap:
                page, continuation=reviews(app_id,lang='en',country='in',sort=Sort.NEWEST,
                    count=min(200,cap-len(rows)),continuation_token=continuation)
                rows.extend(page)
                dates=[x.get('at') for x in page if x.get('at')]
                print(app_id,len(rows),'oldest',min(dates).isoformat() if dates else None,flush=True)
                if not page or not getattr(continuation,'token',None):
                    reason='source_exhausted';break
                if dates and min(dates)<datetime(2025,1,1):
                    reason='requested_window_boundary_reached';break
                time.sleep(.5)
        except Exception as e:
            reason='request_or_parser_failed'; error=str(e)
        dates=[x.get('at') for x in rows if x.get('at')]
        summary.append(dict(app_id=app_id,parsed_review_count=len(rows),unique_review_ids=len({x.get('reviewId') for x in rows}),
            oldest=min(dates).isoformat() if dates else None,newest=max(dates).isoformat() if dates else None,
            stop_reason=reason,error=error,
            note='Original network response bodies are preserved. Parser counts are collection QA, not cleaned analysis. Country parameter does not prove every reviewer lives in India.'))
    (ROOT/'data/manifests/review_coverage.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
