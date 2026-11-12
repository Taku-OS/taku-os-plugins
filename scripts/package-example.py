#!/usr/bin/env python3
"""Build the source-controlled Hello World sample with deterministic ZIP metadata."""
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

root = Path(__file__).resolve().parents[1]
source = root / 'examples/taku-hello-world'
manifest = json.loads((source / '.codex-plugin/plugin.json').read_text())
name, version = manifest['name'], manifest['version']
if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', name):
    raise SystemExit('Invalid plugin name')
if not isinstance(version, str) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[-.][A-Za-z0-9.-]+)?', version):
    raise SystemExit('Invalid plugin version')
package = root / 'packages' / f'{name}-{version}.zip'
index = root / 'index' / name / f'{version}.json'
for destination, parent in [(package, root / 'packages'), (index, root / 'index')]:
    if parent.is_symlink() or destination.is_symlink():
        raise SystemExit('Output paths may not be symlinks')
    destination.resolve().relative_to(parent.absolute())
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
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
archive_bytes = buffer.getvalue()
record.update(package=package.relative_to(root).as_posix(), sha256=hashlib.sha256(archive_bytes).hexdigest())
index_bytes = (json.dumps(record, indent=2) + '\n').encode()
for destination, data in [(package, archive_bytes), (index, index_bytes)]:
    if destination.exists() and destination.read_bytes() != data:
        raise SystemExit('Published version differs; bump the version instead of overwriting it')
for destination, data in [(package, archive_bytes), (index, index_bytes)]:
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(data)
print(package.relative_to(root), record['sha256'])
