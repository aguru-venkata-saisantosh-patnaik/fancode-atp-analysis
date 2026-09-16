"""Shared offline I/O and visual conventions. Statistical calculations live in notebooks."""
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
logging.getLogger('pypdf').setLevel(logging.ERROR)
ROOT=Path(__file__).resolve().parents[1]
SOURCES={x['id']:x for x in json.loads((ROOT/'data/manifests/sources.json').read_text())}
CAPTURES={x['id']:x for x in json.loads((ROOT/'data/manifests/manual_captures.json').read_text())}
METRICS={x['metric_id']:x for x in json.loads((ROOT/'config/external_evidence_registry.json').read_text())['metrics']}
COLORS=['#1565C0','#00A69C','#FF9F1C','#D94B64','#7755BB','#6C7A89']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.titlesize':14,'figure.facecolor':'white','axes.facecolor':'white','axes.prop_cycle':plt.cycler(color=COLORS),'svg.fonttype':'none','savefig.bbox':'tight'})
pd.set_option('display.max_columns',18);pd.set_option('display.max_rows',25);pd.set_option('display.float_format',lambda x:f'{x:,.3f}')

def path(id):return ROOT/(SOURCES.get(id) or CAPTURES[id])['file']
def rawjson(id):return json.loads(path(id).read_text())
def text(id,page=None):
 p=path(id)
 if p.read_bytes().startswith(b'%PDF'):
  d=PdfReader(p)
  return d.pages[page-1].extract_text() if page else '\n'.join(x.extract_text() or '' for x in d.pages)
 s=p.read_text()
 return BeautifulSoup(s,'html.parser').get_text(' ',strip=True) if '<html' in s[:5000].lower() else s

def table(df,name,processed=False):
 folder=ROOT/('data/processed' if processed else 'outputs/tables');folder.mkdir(parents=True,exist_ok=True)
 df.to_csv(folder/(name+'.csv'),index=False)
 return df

def fig(name,subtitle=None):
 f=plt.gcf()
 if subtitle:f.text(.01,-.035,subtitle,fontsize=8,color='#526170',wrap=True)
 for ext in ['png','svg']:f.savefig(ROOT/f'outputs/figures/{ext}/{name}.{ext}',dpi=220)
 display(f);plt.close(f)

def source_table(ids):
 return pd.DataFrame([{'source_id':i,'url':(SOURCES.get(i) or CAPTURES[i]).get('url',(SOURCES.get(i) or CAPTURES[i]).get('source_url')),'raw_file':str(path(i).relative_to(ROOT))} for i in ids])

def report(name,content):
 (ROOT/'outputs/reports'/f'{name}.md').write_text('# '+name.replace('_',' ')+'\n\nAuthor: Competition team\n\n'+content+'\n')

def read(name):return pd.read_csv(ROOT/'data/processed'/f'{name}.csv')
