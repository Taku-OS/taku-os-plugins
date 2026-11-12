#!/usr/bin/env python3
"""Submit an existing device-side taku-plugin publish result using host gh credentials."""
import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path


def run(*args, cwd=None):
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed (exit {result.returncode})')
    return result.stdout.strip()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--serial', required=True)
parser.add_argument('--packed', help='Existing device output directory returned by taku-plugin publish')
parser.add_argument('--source', help='Device plugin source directory; requires --output')
parser.add_argument('--output', help='New device output directory; requires --source')
parser.add_argument('--device-cli', default='/system_ext/bin/taku-plugin', help='Absolute device CLI path')
parser.add_argument('--repo', default='Taku-OS/taku-os-plugins')
parser.add_argument('--example', action='store_true')
args = parser.parse_args()
if bool(args.source) != bool(args.output) or bool(args.packed) == bool(args.source):
    parser.error('provide --packed or both --source and --output')
packed = args.packed or args.output
result = {'published': False, 'device_output': packed}
try:
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        raise ValueError('Invalid repository')
    if not packed.startswith('/') or (args.source and not args.source.startswith('/')) or not args.device_cli.startswith('/'):
        raise ValueError('Device paths must be absolute')
    if args.source:
        command = shlex.join([args.device_cli, 'publish', args.source, packed, args.repo])
        device_result = json.loads(run('adb', '-s', args.serial, 'shell', command))
        if device_result.get('published'):
            print(json.dumps(device_result, ensure_ascii=False))
            raise SystemExit(0)
    with tempfile.TemporaryDirectory(prefix='taku-submit-') as temp:
        temp = Path(temp)
        run('adb', '-s', args.serial, 'pull', packed + '/.', str(temp / 'packed'))
        records = list((temp / 'packed' / 'index').glob('*/*.json'))
        if len(records) != 1:
            raise ValueError('Expected exactly one index record')
        record = json.loads(records[0].read_text())
        name, version = record['name'], record['version']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', name) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:[-.][A-Za-z0-9.-]+)?', version):
            raise ValueError('Invalid plugin name or version')
        package = temp / 'packed' / (name + '-' + version + '.zip')
        if records[0].relative_to(temp / 'packed').as_posix() != f'index/{name}/{version}.json' or record['package'] != f'packages/{package.name}':
            raise ValueError('Unexpected package or index path')
        if hashlib.sha256(package.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Package hash mismatch')
        result.update(name=name, version=version, sha256=record['sha256'])
        owner = run('gh', 'api', 'user', '--jq', '.login')
        run('gh', 'repo', 'fork', args.repo, '--clone=false')
        fork = owner + '/' + args.repo.split('/')[1]
        parent = run('gh', 'api', 'repos/' + fork, '--jq', '.parent.full_name')
        if parent.lower() != args.repo.lower():
            raise ValueError('Existing fork does not belong to the requested repository')
        checkout = temp / 'checkout'
        run('gh', 'repo', 'clone', fork, str(checkout))
        run('git', 'fetch', 'https://github.com/' + args.repo + '.git', 'main', cwd=checkout)
        branch = 'plugin/' + name + '-' + uuid.uuid4().hex[:8]
        run('git', 'checkout', '-b', branch, 'FETCH_HEAD', cwd=checkout)
        destination = checkout / 'packages' / package.name
        index = checkout / 'index' / name / (version + '.json')
        if destination.exists() or index.exists():
            raise ValueError('This plugin version already exists')
        destination.parent.mkdir(parents=True, exist_ok=True)
        index.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(package, destination)
        shutil.copyfile(records[0], index)
        run('git', 'add', str(destination.relative_to(checkout)), str(index.relative_to(checkout)), cwd=checkout)
        title = ('[example] ' if args.example else '') + f'Add plugin {name} {version}'
        run('git', 'commit', '-m', title, cwd=checkout)
        run('git', 'push', 'origin', branch, cwd=checkout)
        result.update(branch=branch, fork=fork)
        result['pr'] = run('gh', 'pr', 'create', '--repo', args.repo, '--head', owner + ':' + branch,
                           '--title', title, '--body', 'Community plugin package and index entry. Review the package and its declared capabilities and permissions.', cwd=checkout)
        result['published'] = True
except (OSError, ValueError, KeyError, RuntimeError, subprocess.TimeoutExpired) as error:
    result['reason'] = str(error)
print(json.dumps(result, ensure_ascii=False))
raise SystemExit(0 if result['published'] else 1)
