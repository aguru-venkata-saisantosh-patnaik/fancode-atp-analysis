"""Offline integrity, format and collection-coverage checks.

This does not clean text, classify sentiment, convert schedules or fit models.
Provider bodies are read-only. QA outputs go to data/manifests.
"""
import hashlib
import csv
import io
import json
import logging
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup
from pypdf import PdfReader
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs

ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'data/manifests'
logging.getLogger('pypdf').setLevel(logging.ERROR)
def readjson(name):return json.loads((M/name).read_text())
def jsonlines(name):return [json.loads(x) for x in (M/name).read_text().splitlines() if x.strip()]
def write(name,value):(M/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def main():
    logs=jsonlines('collection_log.jsonl')+jsonlines('review_collection_log.jsonl')+readjson('local_inputs.json')+readjson('manual_captures.json')
    inventory=[];errors=[];byfile=defaultdict(list)
    for row in logs:
        if not row.get('file'):continue
        byfile[row['file']].append(row)
        p=ROOT/row['file']
        if not p.exists():errors.append({'file':row['file'],'error':'missing'});continue
        data=p.read_bytes()
        if hashlib.sha256(data).hexdigest()!=row['sha256']:errors.append({'file':row['file'],'error':'checksum mismatch'})
        if len(data)!=row['bytes']:errors.append({'file':row['file'],'error':'size mismatch'})
    for p in sorted((ROOT/'data/raw').rglob('*')):
        if not p.is_file() or p.name=='README.md':continue
        rel=str(p.relative_to(ROOT));data=p.read_bytes()
        item=dict(file=rel,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),source_ids=sorted({x['id'] for x in byfile[rel]}))
        if not byfile[rel]:errors.append({'file':rel,'error':'orphan without provenance'})
        try:
            if data.startswith(b'%PDF'):
                pdf=PdfReader(p);item.update(format='PDF',page_count=len(pdf.pages),text_layer_characters=sum(len(x.extract_text() or '') for x in pdf.pages))
                if not len(pdf.pages):errors.append({'file':rel,'error':'zero-page PDF'})
            elif 'google_play' in rel:
                match=json.loads(Regex.REVIEWS.findall(data.decode())[0]);body=json.loads(match[0][2])
                item.update(format='Google Play public RPC',review_count=len(body[0]) if body and body[0] else 0)
            elif p.suffix == '.csv' and '_failed_requests' not in rel:
                records=list(csv.reader(io.StringIO(data.decode('utf-8-sig'))))
                if len(records)<2 or len(records[0])<2:raise ValueError('CSV lacks header or data')
                widths={len(r) for r in records}
                if len(widths)!=1:raise ValueError('Inconsistent CSV row widths')
                item.update(format='CSV',data_rows=len(records)-1,columns=records[0])
            elif p.name.startswith('google_trends_daily_table_v2__'):
                table=data.decode();rows=list(csv.reader(io.StringIO(table),delimiter='\t'))
                fnv=2166136261
                for char in table:fnv=((fnv^ord(char))*16777619)&0xffffffff
                if fnv!=0x8edf4d2d or len(table)!=5587:raise ValueError('Transcription differs from browser DOM checksum')
                dates=[datetime.strptime(r[0],'%b %d, %Y').date() for r in rows[1:]]
                if len(dates)!=255 or any((b-a).days!=1 for a,b in zip(dates,dates[1:])):raise ValueError('Missing or repeated daily date')
                if any(len(r)!=5 for r in rows) or any(not 0<=int(x)<=100 for r in rows[1:] for x in r[1:]):raise ValueError('Invalid trend values')
                item.update(format='Browser table TSV',data_rows=255,series=4,transcription_check='PASS')
            else:
                try:
                    obj=json.loads(data);item['format']='JSON'
                    if isinstance(obj,dict) and 'feed' in obj:
                        entries=obj['feed'].get('entry',[])
                        if isinstance(entries,dict):entries=[entries]
                        item['review_count']=sum('im:rating' in e for e in entries)
                except (ValueError,UnicodeDecodeError):
                    if b'<html' in data[:5000].lower() or b'<!doctype html' in data[:5000].lower():
                        soup=BeautifulSoup(data,'html.parser');item.update(format='HTML',title=soup.title.get_text(' ',strip=True) if soup.title else None,visible_text_characters=len(soup.get_text(' ',strip=True)))
                    else:item['format']='Text or JavaScript'
        except Exception as e:
            item.setdefault('format','Unparsed')
            item['parse_error']=type(e).__name__+': '+str(e)[:150]
            if '_failed_requests' not in rel:errors.append({'file':rel,'error':item['parse_error']})
        inventory.append(item)
    write('raw_inventory.json',inventory)
    # Review QA counts are based on source records. No text or names are exported.
    apps=defaultdict(dict);occurrences=Counter()
    for row in jsonlines('review_collection_log.jsonl'):
        if not str(row['http_status']).startswith('2'):continue
        dom=(ROOT/row['file']).read_text();match=json.loads(Regex.REVIEWS.findall(dom)[0]);body=json.loads(match[0][2])
        for review in body[0] if body and body[0] else []:
            rid=ElementSpecs.Review['reviewId'].extract_content(review)
            # Raw UNIX time, explicit India timezone avoids host-dependent date filtering.
            epoch=review[5][0];dt=datetime.fromtimestamp(epoch,ZoneInfo('Asia/Kolkata'))
            apps[row['app_id']][rid]=dt;occurrences[row['app_id']]+=1
    for row in readjson('sources.json'):
        if not row['id'].startswith('fancode_ios_reviews_page') or row['retrieval_status']=='retrieval_failed':continue
        feed=json.loads((ROOT/row['file']).read_text())['feed'];entries=feed.get('entry',[])
        if isinstance(entries,dict):entries=[entries]
        for e in entries:
            if 'im:rating' not in e:continue
            apps['ios_1406379831'][e['id']['label']]=datetime.fromisoformat(e['updated']['label']).astimezone(ZoneInfo('Asia/Kolkata'))
            occurrences['ios_1406379831']+=1
    start=datetime(2025,1,1,tzinfo=ZoneInfo('Asia/Kolkata'));end=datetime(2026,9,13,tzinfo=ZoneInfo('Asia/Kolkata'))
    coverage=[]
    for app,entries in apps.items():
        dates=list(entries.values())
        coverage.append(dict(app_id=app,raw_record_occurrences=occurrences[app],unique_review_ids=len(entries),within_registered_window=sum(start<=d<end for d in dates),before_window=sum(d<start for d in dates),after_window=sum(d>=end for d in dates),earliest=min(dates).isoformat(),latest=max(dates).isoformat(),timezone='Asia/Kolkata',note='Accessible storefront reviews, not a representative customer sample. iOS uses public updated timestamp.'))
    write('review_window_qa.json',coverage)
    src=readjson('sources.json');dup=defaultdict(list)
    for x in inventory:dup[x['sha256']].append(x['file'])
    summary=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),result='PASS' if not errors else 'FAIL',errors=errors,raw_files=len(inventory),raw_bytes=sum(x['bytes'] for x in inventory),http_source_ids=len(src),http_retrieved=sum(x['retrieval_status']=='retrieved_unvalidated' for x in src),http_failed=sum(x['retrieval_status']=='retrieval_failed' for x in src),local_input_files=len(readjson('local_inputs.json')),browser_observations=len(readjson('manual_captures.json')),formats=dict(Counter(x['format'] for x in inventory)),duplicate_content_groups=[v for v in dup.values() if len(v)>1],review_coverage=coverage,note='PASS means byte integrity and expected file formats, not completeness, causal validity or approval for publication. Consult source_validation.json and docs/DATA_AVAILABILITY.md.')
    write('validation_report.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['duplicate_content_groups','review_coverage']},indent=2))
    print('Review counts:',[(x['app_id'],x['unique_review_ids'],x['within_registered_window']) for x in coverage])
    if errors:raise SystemExit(1)
if __name__=='__main__':main()
