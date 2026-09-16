"""Check public channel-search snapshots without estimating demand."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'data/manifests'
def main():
    sources={x['id']:x for x in json.loads((M/'sources.json').read_text())};report=[];all_ids=set()
    for i in ['fancode_youtube_tennis_search','fancode_youtube_atp_search']:
        text=(ROOT/sources[i]['file']).read_text();match=re.search(r'(?:var )?ytInitialData\s*=\s*',text)
        if not match:raise ValueError('Missing public channel data: '+i)
        obj,_=json.JSONDecoder().raw_decode(text[match.end():]);videos=[]
        def walk(x):
            if isinstance(x,dict):
                for renderer in ['videoRenderer','channelVideoPlayerRenderer']:
                    if renderer in x:videos.append(x[renderer])
                for y in x.values():walk(y)
            elif isinstance(x,list):
                for y in x:walk(y)
        walk(obj.get('contents',{}));channel=obj['metadata']['channelMetadataRenderer']
        assert channel['externalId']=='UCF10AG_t1AYW3mlmX7g1VJA'
        ids={v['videoId'] for v in videos};all_ids|=ids
        report.append(dict(source_id=i,channel=channel['title'],channel_id=channel['externalId'],video_renderers=len(videos),unique_video_ids=len(ids),with_displayed_views=sum('viewCountText' in v for v in videos),with_relative_publication_label=sum('publishedTimeText' in v for v in videos),note='Initial ranked keyword results only. Not a census or India-specific viewership. Relative publication labels are not precise timestamps.'))
    result=dict(snapshots=report,unique_video_ids_across_queries=len(all_ids),scope='Metadata only. No video or image files downloaded. No views-to-payers inference.')
    (M/'video_source_qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
