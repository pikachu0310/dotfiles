#!/usr/bin/env python3
"""Create private context templates at an explicit destination, preserving existing files."""
import argparse,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
d=a.destination.expanduser().resolve()
if d==root.parent or root.parent in d.parents:raise SystemExit('Private context must be outside the public package')
if a.destination.is_symlink():raise SystemExit('Refusing a linked destination')
d.mkdir(parents=True,exist_ok=True);created=[];kept=[]
for n in ['ME','PERSONAL','PROJECTS','CANDIDATES']:
 target=d/(n+'.md')
 if target.exists():kept.append(n);continue
 try:
  with target.open('xb') as f:f.write((root/'context/examples'/(n+'.example.md')).read_bytes())
  created.append(n)
 except FileExistsError:kept.append(n)
print(json.dumps({'created':created,'kept':kept,'destination':str(d)},ensure_ascii=False))
