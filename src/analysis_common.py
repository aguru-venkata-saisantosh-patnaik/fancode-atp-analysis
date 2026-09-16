"""Offline source access, exports and chart conventions for the competition notebooks."""
from pathlib import Path
import os,json,re,hashlib,logging
os.environ.setdefault('MPLCONFIGDIR','/tmp/fancode-mpl-cache')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pypdf import PdfReader
from bs4 import BeautifulSoup
from IPython.display import display,Markdown
logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT=Path(__file__).resolve().parents[1]
SOURCES={x['id']:x for x in json.loads((ROOT/'data/manifests/sources.json').read_text())}
CAPTURES={x['id']:x for x in json.loads((ROOT/'data/manifests/manual_captures.json').read_text())}
METRICS={x['metric_id']:x for x in json.loads((ROOT/'config/external_evidence_registry.json').read_text())['metrics']}
ACTIVE_NOTEBOOK='interactive'
ACTIVE_SOURCES=[]
CFG=json.loads((ROOT/'analysis_config/analysis.json').read_text())
COLORS=['#1264BA','#00A398','#F49D19','#D54B65','#7853B5','#64748B']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.titlesize':13,'figure.facecolor':'white','axes.facecolor':'white','axes.prop_cycle':plt.cycler(color=COLORS),'svg.fonttype':'none','savefig.bbox':'tight'})
pd.set_option('display.max_columns',18);pd.set_option('display.max_rows',24);pd.set_option('display.float_format',lambda x:f'{x:,.3f}')
def path(i):return ROOT/(SOURCES.get(i) or CAPTURES[i])['file']
def rawjson(i):return json.loads(path(i).read_text())
def text(i,page=None):
 p=path(i)
 if p.read_bytes().startswith(b'%PDF'):
  d=PdfReader(p);return (d.pages[page-1].extract_text() or '') if page else '\n'.join(x.extract_text() or '' for x in d.pages)
 s=p.read_text();return BeautifulSoup(s,'html.parser').get_text(' ',strip=True) if '<html' in s[:5000].lower() else s

def trace(p,kind,note=''):
 q=ROOT/'outputs/validation/artifact_trace.jsonl';q.parent.mkdir(parents=True,exist_ok=True)
 with q.open('a') as f:f.write(json.dumps({'artifact':str(p.relative_to(ROOT)),'kind':kind,'notebook':ACTIVE_NOTEBOOK,'source_ids':ACTIVE_SOURCES,'note':note,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})+'\n')

def table(df,name,processed=False):
 folder=ROOT/('data/processed' if processed else 'outputs/tables');folder.mkdir(parents=True,exist_ok=True);p=folder/(name+'.csv');df.to_csv(p,index=False);trace(p,'processed table' if processed else 'output table');return df

def fig(name,note=''):
 f=plt.gcf()
 f.tight_layout(pad=1.3)
 if note:f.text(.01,-.025,note,fontsize=8,color='#526170',wrap=True)
 for ext in ['png','svg']:
  p=ROOT/f'outputs/figures/{ext}';p.mkdir(parents=True,exist_ok=True);f.savefig(p/f'{name}.{ext}',dpi=200);trace(p/f'{name}.{ext}','figure',note)
 display(f);plt.close(f)

def source_table(ids):
 rows=[]
 for i in dict.fromkeys(ids):
  s=SOURCES.get(i) or CAPTURES[i];rows.append({'source_id':i,'url':s.get('url',s.get('source_url')),'raw_file':str(path(i).relative_to(ROOT)),'retrieved':s.get('retrieved_at_utc',s.get('recorded_at_utc'))})
 return pd.DataFrame(rows)
def report(name,body):
 p=ROOT/'outputs/reports'/f'{name}.md';p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# '+name.replace('_',' ')+'\n\nAuthor: Chanakya\n\n'+body+'\n')
def read(name):return pd.read_csv(ROOT/'data/processed'/f'{name}.csv')
def check(name,checks):
 checks={k:bool(v) for k,v in checks.items()}
 assert all(checks.values()),checks
 p=ROOT/'outputs/validation'/f'{name}.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'result':'PASS','checks':checks},indent=2)+'\n');display(pd.DataFrame(list(checks.items()),columns=['check','passed']))
