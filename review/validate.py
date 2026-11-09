#!/usr/bin/env python3
"""Check publication bodies, evidence and immutable case links offline."""
from pathlib import Path
import hashlib,json,subprocess
r=Path(__file__).resolve().parents[1]
m=json.loads((r/'memory/manifest.json').read_text());ledger=json.loads((r/'review/revisions.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
normalized=lambda b:hashlib.sha256(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest()
base=ledger['base_commit'];old=json.loads(subprocess.check_output(['git','-C',str(r),'show',base+':memory/manifest.json']))
assert set(old['lessons'])==set(m['lessons']);assert len(m['lessons'])==521
assert set(m['files'])=={str(p.relative_to(r/'memory')) for p in (r/'memory').rglob('*') if p.is_file() and p.name!='manifest.json'}
assert all(sha(r/'memory'/p)==digest for p,digest in m['files'].items())
changed=set();links=0
for mid,lesson in m['lessons'].items():
 assert lesson['path']==old['lessons'][mid]['path'];assert lesson['evidence']==old['lessons'][mid]['evidence']
 previous=subprocess.check_output(['git','-C',str(r),'show',base+':memory/'+lesson['path']])
 if previous!=(r/'memory'/lesson['path']).read_bytes():changed.add(mid)
 for ev in lesson['evidence']:
  assert (r/'store/cases'/ev['case']/(ev['revision']+'.json')).is_file();links+=1
assert len(changed)==137 and len(m['lessons'])-len(changed)==384
assert changed=={x['id'] for x in ledger['items']}
refs=0
for entry in ledger['items']:
 body=(r/'review'/entry['path']).resolve();assert body.is_relative_to(r/'memory');assert normalized(body.read_bytes())==entry['revised_sha256']
 for ev in entry['sources']:
  p=(r/'review'/ev['path']).resolve();assert p.is_relative_to(r/'review/evidence');assert sha(p)==ev['sha256'];refs+=1
assert (r/'memory'/m['audit_sidecar']).resolve()==r/'review/revisions.json'
print(json.dumps({'lessons':521,'changed':137,'unchanged':384,'file_hashes':len(m['files']),'case_bindings':links,'revision_evidence_refs':refs,'status':'pass'}))
