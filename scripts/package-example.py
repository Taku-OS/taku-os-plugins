#!/usr/bin/env python3
"""Build the source-controlled Hello World sample with deterministic ZIP metadata."""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
source = root / 'examples/taku-hello-world'
manifest = json.loads((source / '.codex-plugin/plugin.json').read_text())
name, version = manifest['name'], manifest['version']
package = root / 'packages' / f'{name}-{version}.zip'
package.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(source.rglob('*')):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit('Example may not contain symlinks')
        info = zipfile.ZipInfo(name + '/' + path.relative_to(source).as_posix(), (2026, 11, 12, 0, 0, 0))
        info.create_system = 3
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100755 if path.name == 'server.sh' else 0o100644) << 16
        archive.writestr(info, path.read_bytes())
record = {key: manifest[key] for key in ['name', 'version', 'description', 'author', 'taku']}
record.update(package=package.relative_to(root).as_posix(), sha256=hashlib.sha256(package.read_bytes()).hexdigest())
index = root / 'index' / name / f'{version}.json'
index.parent.mkdir(parents=True, exist_ok=True)
index.write_text(json.dumps(record, indent=2) + '\n')
print(package.relative_to(root), record['sha256'])
