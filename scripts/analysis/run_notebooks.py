"""Execute saved notebooks against local raw files, retain outputs and HTML exports."""
from pathlib import Path
import os,sys,json,time,argparse,hashlib
R=Path(__file__).resolve().parents[2]
os.environ.setdefault('MPLCONFIGDIR','/tmp/fancode-mpl-cache')
os.environ.setdefault('IPYTHONDIR','/tmp/fancode-ipython')
os.environ.setdefault('JUPYTER_PATH','/private/tmp/fancode-jupyter/share/jupyter')
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');p.add_argument('--kernel',default='fancode-analysis');a=p.parse_args()
logpath=R/'outputs/validation/execution_log.json';logs=json.loads(logpath.read_text()) if logpath.exists() else {}
for path in sorted((R/'notebooks/source').glob('*.ipynb')):
 if a.only and path.stem.split('_')[0] not in a.only:continue
 print('RUN',path.name,flush=True);start=time.time();nb=nbformat.read(path,as_version=4)
 try:
  NotebookClient(nb,timeout=900,kernel_name=a.kernel,resources={'metadata':{'path':str(R)}},record_timing=True).execute()
  errors=[o for c in nb.cells if c.cell_type=='code' for o in c.get('outputs',[]) if o.output_type=='error'];assert not errors
  nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
  output=R/'notebooks/executed'/path.name;nbformat.write(nb,output)
  html,_=HTMLExporter(template_name='lab').from_notebook_node(nb)
  (R/'outputs/reports'/f'{path.stem}.html').write_text(html)
  logs[path.stem]={'status':'PASS','seconds':round(time.time()-start,2),'code_cells':sum(c.cell_type=='code' for c in nb.cells),'executed_cells':sum(c.cell_type=='code' and c.execution_count is not None for c in nb.cells),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'executed_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
  print('PASS',path.name,logs[path.stem]['seconds'],'seconds',flush=True)
 except Exception as e:
  logs[path.stem]={'status':'FAIL','error_type':type(e).__name__};logpath.write_text(json.dumps(logs,indent=2)+'\n');raise
 logpath.write_text(json.dumps(logs,indent=2)+'\n')
