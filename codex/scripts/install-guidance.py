#!/usr/bin/env python3
"""Preview or create global guidance without overwriting an existing different AGENTS.md."""
import argparse,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--home',type=Path,required=True);p.add_argument('--context-root',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
h=a.home.expanduser().absolute();c=a.context_root.expanduser().resolve();target=h/'.codex/AGENTS.md'
if h.is_symlink() or (h/'.codex').is_symlink() or target.is_symlink():raise SystemExit('Refusing linked guidance destination')
if root.parent==c or root.parent in c.parents:raise SystemExit('Private context must be outside the public package')
data=(root/'config/AGENTS.global.md').read_text().replace('<OPS_ROOT>',str(root)).replace('<PRIVATE_CONTEXT_ROOT>',str(c)).encode()
if target.exists() and target.read_bytes()!=data:raise SystemExit('Existing guidance differs; merge the concrete template manually. Nothing written.')
if a.apply and not target.exists():
 target.parent.mkdir(parents=True,exist_ok=True)
 with target.open('xb') as f:f.write(data)
print(json.dumps({'mode':'apply' if a.apply else 'preview','target':str(target),'context_root':str(c),'status':'matches' if target.exists() else 'would-create'}))
