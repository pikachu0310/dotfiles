#!/usr/bin/env python3
"""Read-only grouped review of the declared public payload; no secrets are printed."""
import hashlib,json,re,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
lock_path=root/'config/files.lock.json'
issues=[]
def flag(path,line,reason):issues.append({'file':str(path),'line':line,'reason':reason})
try:lock=json.loads(lock_path.read_text())
except (OSError,ValueError):raise SystemExit('Missing or invalid reviewed publication file manifest')
if set(lock) != {'reviewed_at','readme_sha256','files','repository_files'}:flag('config/files.lock.json',0,'unexpected publication manifest field')
if not isinstance(lock.get('files'),dict):raise SystemExit('Invalid file manifest')
for name,digest in lock['files'].items():
 if not isinstance(digest,str) or not re.fullmatch(r'[0-9a-f]{64}',digest):flag('config/files.lock.json',0,'invalid content digest')
 if Path(name).is_absolute() or '..' in Path(name).parts:flag('config/files.lock.json',0,'invalid publication path')
expected=lock['files']
readme=root.parent/'README.md'
if not readme.is_file() or hashlib.sha256(readme.read_bytes()).hexdigest()!=lock.get('readme_sha256'):flag('../README.md',0,'reviewed human entry differs or is missing')
actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and p!=lock_path}
for rel,p in actual.items():
 if rel not in expected:flag(rel,0,'undeclared publication file');continue
 if p.is_symlink():flag(rel,0,'symlink publication input');continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected[rel]:flag(rel,0,'reviewed file hash differs')
 for parent in p.parents:
  if parent==root:break
  if parent.is_symlink():flag(rel,0,'linked directory in publication input')
for rel in expected:
 if rel not in actual:flag(rel,0,'reviewed publication file is missing')
patterns=[
 ('API credential',re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b')),
 ('GitHub credential',re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{25,})\b')),
 ('AWS credential',re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
 ('Slack credential',re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b')),
 ('private key material',re.compile(r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----')),
 ('private thread link',re.compile(r'codex://threads/[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}')),
 ('concrete home path',re.compile(r'/home/(?!<|example(?:/|\b)|user(?:/|\b))[A-Za-z0-9_][A-Za-z0-9_.-]*')),
 ('concrete Windows profile',re.compile(r'(?:[A-Za-z]:[/\\]|/mnt/[a-z]/)Users[/\\](?!<|example(?:[/\\]|\b)|USER(?:[/\\]|\b))[A-Za-z0-9_.-]+',re.I)),
]
for rel,p in actual.items():
 parts=Path(rel).parts
 if any(x in ['__pycache__','node_modules','sessions','logs','cache','personal'] for x in parts) or p.suffix in ['.db','.sqlite','.sqlite3','.pyc','.pyo'] or p.name in ['auth.json','ops-profile.json','config.toml','.env','agent_config.json']:
  flag(rel,0,'private or runtime publication input')
 if rel.startswith('context/') and not rel.startswith('context/examples/'):flag(rel,0,'non-example personal context')
 try:text=p.read_text(encoding='utf-8')
 except UnicodeDecodeError:
  if not (rel.startswith('.agents/skills/yomiyasu/assets/') and p.suffix=='.png'):flag(rel,0,'unreviewed binary payload')
  continue
 for n,line in enumerate(text.splitlines(),1):
  for reason,pattern in patterns:
   if pattern.search(line):flag(rel,n,reason)
# Review shell dotfiles and their documentation with the same credential rules.
repo=root.parent
repository_expected=lock.get('repository_files',{})
if not isinstance(repository_expected,dict):raise SystemExit('Invalid repository file manifest')
repository_actual={}
for directory in [repo/'.config',repo/'docs']:
 if directory.exists():
  repository_actual.update({p.relative_to(repo).as_posix():p for p in directory.rglob('*') if p.is_file()})
for name in ['.gitconfig','.gitignore']:
 if (repo/name).is_file():repository_actual[name]=repo/name
for rel,digest in repository_expected.items():
 if Path(rel).is_absolute() or '..' in Path(rel).parts or rel not in repository_actual:flag(rel,0,'invalid or missing repository publication file');continue
 if not isinstance(digest,str) or not re.fullmatch(r'[0-9a-f]{64}',digest):flag(rel,0,'invalid repository content digest')
for rel,p in repository_actual.items():
 if rel not in repository_expected:flag(rel,0,'undeclared repository publication file');continue
 if p.is_symlink() or any(parent.is_symlink() for parent in p.parents if parent!=repo and repo in parent.parents):flag(rel,0,'linked repository publication input');continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=repository_expected[rel]:flag(rel,0,'reviewed repository file hash differs')
 try:text=p.read_text(encoding='utf-8')
 except UnicodeDecodeError:flag(rel,0,'unreviewed repository binary');continue
 for n,line in enumerate(text.splitlines(),1):
  for reason,pattern in patterns:
   if pattern.search(line):flag(rel,n,reason)

# Parse package metadata without accessing authenticated host configuration.
for rel,p in actual.items():
 if p.suffix=='.json':
  try:json.loads(p.read_text())
  except ValueError:flag(rel,0,'invalid JSON')
names=[]
for p in root.rglob('SKILL.md'):
 t=p.read_text();m=re.search(r'^name:\s*[\"\x27]?([^\"\x27\r\n]+)',t,re.M)
 if not m or not re.search(r'^description:',t,re.M):flag(p.relative_to(root),0,'missing skill discovery metadata')
 else:names.append(m.group(1).strip())
for n in set(names):
 if names.count(n)>1:flag('SKILL.md',0,'duplicate skill name: '+n)
for rel in ['.agents/plugins/marketplace.json','plugins/codex-intent/plugin.json','plugins/codex-intent/.codex-plugin/plugin.json','config/personal-skills.json','config/research-tools.json','config/AGENTS.global.md']:
 if rel not in actual:flag(rel,0,'required distribution file missing')
print(json.dumps({'ok':not issues,'files':len(actual),'repository_files':len(repository_actual),'skill_entries':len(names),'issues':issues,'boundary':'declared public package only; no claim of exhaustive semantic privacy detection'},ensure_ascii=False,indent=2))
raise SystemExit(1 if issues else 0)
