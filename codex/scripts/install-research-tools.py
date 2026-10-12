#!/usr/bin/env python3
"""Install reviewed public release assets into an explicitly selected user's bin folder."""
import argparse,hashlib,io,json,os,platform,tarfile,tempfile,urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');p.add_argument('--bin',type=Path,default=Path.home()/'.local/bin');a=p.parse_args()
system=platform.system();machine=platform.machine().lower()
if system not in ['Windows','Linux'] or machine not in ['x86_64','amd64']:raise SystemExit('No reviewed asset for this OS/architecture; inspect upstream instead.')
manifest=json.loads((root/'config/research-tools.json').read_text());plan=[]
for tool in manifest['tools']:
 for asset in tool['assets']:
  if ('windows' if system=='Windows' else 'linux') not in asset['asset']:continue
  name='agtlog' if tool['repository'].endswith('/agtlog') else ('ax.exe' if system=='Windows' else 'ax')
  expected=manifest['agtlog_binary_sha256'] if name=='agtlog' else asset['sha256']
  target=a.bin.expanduser().absolute()/name
  if any(q.is_symlink() for q in [target,*target.parents]):raise SystemExit('Refusing linked binary destination')
  if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise SystemExit('An existing different binary would be overwritten: '+str(target))
  plan.append((tool,asset,target,expected))
print(json.dumps({'mode':'apply' if a.apply else 'preview','tools':[{'repository':t['repository'],'version':t['version'],'target':str(dst)} for t,asset,dst,sha in plan]},indent=2))
if not a.apply:raise SystemExit(0)
# Download and validate all selected assets before writing any destination.
ready=[]
for t,asset,dst,expected in plan:
 if dst.exists():continue
 request=urllib.request.Request(asset['url'],headers={'User-Agent':'Codex-dotfiles-setup'})
 data=urllib.request.urlopen(request,timeout=60).read()
 if hashlib.sha256(data).hexdigest()!=asset['sha256']:raise SystemExit('Release asset checksum mismatch')
 if asset['asset'].endswith('.tar.gz'):
  with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as archive:
   matches=[m for m in archive.getmembers() if m.isfile() and Path(m.name).name=='agtlog']
   if len(matches)!=1:raise SystemExit('Expected exactly one agtlog executable')
   data=archive.extractfile(matches[0]).read()
 if hashlib.sha256(data).hexdigest()!=expected:raise SystemExit('Executable checksum mismatch')
 ready.append((dst,data))
for dst,data in ready:
 dst.parent.mkdir(parents=True,exist_ok=True)
 try:
  with dst.open('xb') as f:f.write(data)
 except FileExistsError:
  if hashlib.sha256(dst.read_bytes()).hexdigest()!=hashlib.sha256(data).hexdigest():raise SystemExit('Destination changed during installation')
 if system=='Linux':dst.chmod(0o755)
print(json.dumps({'installed':[str(dst) for dst,data in ready]}))
