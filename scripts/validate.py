#!/usr/bin/env python3
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / 'plugins/manifest.schema.json').read_text())
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(schema)
packages = set((ROOT / 'packages').glob('*.zip'))
referenced = set()
for index in sorted((ROOT / 'index').glob('*/*.json')):
    record = json.loads(index.read_text())
    name, version = record['name'], record['version']
    assert index.relative_to(ROOT).as_posix() == f'index/{name}/{version}.json'
    package = ROOT / 'packages' / f'{name}-{version}.zip'
    assert record['package'] == package.relative_to(ROOT).as_posix()
    assert package in packages and package not in referenced
    referenced.add(package)
    assert hashlib.sha256(package.read_bytes()).hexdigest() == record['sha256']
    with zipfile.ZipFile(package) as archive:
        entries = archive.infolist()
        paths = [entry.filename for entry in entries]
        assert len(paths) == len(set(paths))
        for entry in entries:
            path = PurePosixPath(entry.filename)
            assert not path.is_absolute() and '..' not in path.parts and '\\' not in entry.filename
            assert path.parts and path.parts[0] == name
            assert not stat.S_ISLNK(entry.external_attr >> 16)
        prefix = name + '/'
        manifest = json.loads(archive.read(prefix + '.codex-plugin/plugin.json'))
        validator.validate(manifest)
        for key in ('name', 'version', 'description', 'taku'):
            assert manifest[key] == record[key]
        if 'author' in manifest:
            assert manifest['author'] == record['author']
        for key in ('skills', 'mcpServers'):
            if key not in manifest:
                continue
            relative = PurePosixPath(manifest[key])
            assert not relative.is_absolute() and '..' not in relative.parts and '\\' not in manifest[key]
            target = prefix + relative.as_posix().rstrip('/')
            if key == 'skills':
                skills = [path for path in paths if path.startswith(target + '/') and path.endswith('/SKILL.md') and len(PurePosixPath(path).parts) == len(PurePosixPath(target).parts) + 2]
                assert skills
                children = {PurePosixPath(path).parts[len(PurePosixPath(target).parts)] for path in paths if path.startswith(target + '/')}
                assert all(f'{target}/{child}/SKILL.md' in paths for child in children)
            else:
                assert isinstance(json.loads(archive.read(target))['mcpServers'], dict)
assert packages == referenced
print(f'Validated {len(referenced)} plugin version(s)')
