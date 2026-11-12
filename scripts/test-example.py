#!/usr/bin/env python3
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
requests = [
    {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05'}},
    {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
    {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'hello_world', 'arguments': {}}},
    {'jsonrpc': '2.0', 'id': 4, 'method': 'unknown'},
]
result = subprocess.run(['/bin/sh', str(root / 'examples/taku-hello-world/server.sh')],
                        input='\n'.join(map(json.dumps, requests)) + '\n',
                        capture_output=True, text=True, check=True, timeout=5)
messages = list(map(json.loads, result.stdout.splitlines()))
assert [m['id'] for m in messages] == [1, 2, 3, 4]
assert messages[1]['result']['tools'][0]['name'] == 'hello_world'
assert messages[2]['result']['content'][0]['text'] == 'Hello from Taku!'
assert messages[3]['error']['code'] == -32601
print('Hello World MCP lifecycle passed (host only).')
