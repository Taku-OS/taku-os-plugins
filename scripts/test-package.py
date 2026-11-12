#!/usr/bin/env python3
"""Exercise path traversal and immutable-version boundaries using isolated fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    candidate = Path(directory) / 'repo'
    (candidate / 'scripts').mkdir(parents=True)
    shutil.copyfile(root / 'scripts/package-example.py', candidate / 'scripts/package-example.py')
    shutil.copytree(root / 'examples', candidate / 'examples')
    manifest_path = candidate / 'examples/taku-hello-world/.codex-plugin/plugin.json'
    manifest = json.loads(manifest_path.read_text())

    def run():
        return subprocess.run([sys.executable, str(candidate / 'scripts/package-example.py')], capture_output=True)

    for name in ['../escape', str(Path(directory) / 'absolute')]:
        manifest_path.write_text(json.dumps({**manifest, 'name': name}))
        assert run().returncode != 0
        assert not (candidate / 'packages').exists()
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    assert run().returncode == 0
    package = next((candidate / 'packages').glob('*.zip'))
    original = package.read_bytes()
    assert run().returncode == 0 and package.read_bytes() == original
    with (candidate / 'examples/taku-hello-world/server.sh').open('a') as stream:
        stream.write('\n# a changed package must have a new version\n')
    assert run().returncode != 0 and package.read_bytes() == original
print('Package traversal rejection and immutable-version tests passed.')
