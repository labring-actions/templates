#!/usr/bin/env python3
"""Check public Steam/RakNet endpoints and authenticated RCON players/save commands.

Usage: PZ_RCON_PASSWORD=... python3 scripts/check_project_zomboid_runtime.py HOST GAME_PORT DIRECT_PORT RCON_PORT
       python3 scripts/check_project_zomboid_runtime.py --check-template  # Requires PyYAML.
"""
import os
import re
import socket
import struct
import sys
import time

MAGIC = bytes.fromhex('00ffff00fefefefefdfdfdfd12345678')


def check_template():
    """Check the dedicated NodePort Service and every startup reference to it."""
    import ast
    from pathlib import Path
    from types import SimpleNamespace
    import yaml

    template = Path(__file__).resolve().parents[1] / 'template/project-zomboid/index.yaml'
    docs = list(yaml.safe_load_all(template.read_text()))
    app = '${{ defaults.app_name }}'
    name = app + '-nodeport'
    services = [doc for doc in docs if doc['kind'] == 'Service']
    assert len(services) == 1
    service = services[0]
    assert service['metadata']['name'] == name and service['spec']['type'] == 'NodePort'
    assert service['metadata']['labels']['app'] == app
    assert service['metadata']['labels']['cloud.sealos.io/app-deploy-manager'] == app
    assert service['spec']['selector'] == {'app': app}
    workload = next(doc for doc in docs if doc['kind'] == 'StatefulSet')
    assert workload['spec']['serviceName'] == name
    role = next(doc for doc in docs if doc['kind'] == 'Role')
    assert role['rules'][0]['resourceNames'] == [name]
    init = workload['spec']['template']['spec']['initContainers'][0]
    assert next(item['value'] for item in init['env'] if item['name'] == 'APP_NAME') == app
    config = next(doc for doc in docs if doc['kind'] == 'ConfigMap')
    script = ast.parse(config['data']['vn-optvn-sealosvn-configurevn-py'])
    url = next(node.value for node in script.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'url' for target in node.targets))
    context = {'os': SimpleNamespace(environ={'APP_NAME': 'test-app', 'POD_NAMESPACE': 'test-namespace'}), '__builtins__': {}}
    resolved = eval(compile(ast.Expression(url), '<initializer-url>', 'eval'), context)
    assert resolved == 'https://kubernetes.default.svc/api/v1/namespaces/test-namespace/services/test-app-nodeport'
    print('NodePort Service references and workload selectors passed')


def receive(sock, count):
    result = bytearray()
    while len(result) < count:
        chunk = sock.recv(count - len(result))
        if not chunk:
            raise RuntimeError('RCON closed the connection')
        result.extend(chunk)
    return bytes(result)


def packet(identifier, kind, text):
    payload = struct.pack('<ii', identifier, kind) + text.encode() + b'\0\0'
    return struct.pack('<i', len(payload)) + payload


def response(sock):
    size = struct.unpack('<i', receive(sock, 4))[0]
    if not 10 <= size <= 1048576:
        raise RuntimeError('Invalid RCON frame size')
    data = receive(sock, size)
    identifier, kind = struct.unpack('<ii', data[:8])
    return identifier, kind, data[8:-2].decode(errors='replace')


def exchange_udp(sock, query, address):
    # UDP delivery is best effort; keep retries bounded and visible.
    for attempt in range(3):
        sock.sendto(query, address)
        try:
            return sock.recvfrom(65535)[0]
        except socket.timeout:
            if attempt == 2:
                raise
            print('UDP response retry ' + str(attempt + 1))


def steam_info(data, expected_port):
    if data[:5] != b'\xff\xff\xff\xffI':
        raise RuntimeError('Game endpoint did not return Steam A2S_INFO')
    offset = 6

    def string():
        nonlocal offset
        end = data.index(0, offset)
        result = data[offset:end].decode(errors='replace')
        offset = end + 1
        return result

    name, world, folder, game = [string() for _ in range(4)]
    if folder != 'zomboid' or game != 'Project Zomboid':
        raise RuntimeError('Steam query returned a different game')
    offset += 9  # App ID, player counts, server type, OS, password flag and VAC.
    string()  # Steam protocol version string.
    flags = data[offset]
    if not flags & 0x80 or struct.unpack_from('<H', data, offset + 1)[0] != expected_port:
        raise RuntimeError('Advertised game port differs from the public endpoint')
    return name, world


def validate_reply(command, message):
    valid = re.match(r'^Players connected \(\d+\):', message) if command == 'players' else message.strip() == 'World saved'
    if not valid:
        raise RuntimeError(command + ' did not return its success response')


def check(host, game_port, direct_port, rcon_port, password):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        query = b'\xff' * 4 + b'TSource Engine Query\0'
        data = exchange_udp(sock, query, (host, game_port))
        if data[:5] == b'\xff' * 4 + b'A':
            data = exchange_udp(sock, query + data[5:9], (host, game_port))
        name, world = steam_info(data, game_port)
        print('game: Steam A2S_INFO, matching advertised port, ' + name + ', ' + world)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        timestamp = struct.pack('>Q', int(time.time() * 1000))
        pong = exchange_udp(sock, b'\x01' + timestamp + MAGIC + b'\0' * 8, (host, direct_port))
        if len(pong) < 33 or pong[0] != 0x1c or pong[1:9] != timestamp or pong[17:33] != MAGIC:
            raise RuntimeError('Direct endpoint did not return a matching RakNet pong')
        print('direct: RakNet pong received')
    with socket.create_connection((host, rcon_port), timeout=30) as sock:
        sock.sendall(packet(1, 3, password))
        for _ in range(3):
            identifier, kind, _ = response(sock)
            if identifier == -1:
                raise RuntimeError('RCON authentication failed')
            if kind == 2 and identifier == 1:
                break
        else:
            raise RuntimeError('RCON authentication was not acknowledged')
        print('RCON authentication: passed')
        for identifier, command in ((2, 'players'), (3, 'save')):
            sock.sendall(packet(identifier, 2, command))
            reply_id, kind, message = response(sock)
            if reply_id != identifier or kind != 0:
                raise RuntimeError(command + ' returned an invalid response frame')
            validate_reply(command, message)
            print(command + ': ' + message.strip())


if __name__ == '__main__':
    if sys.argv[1:] == ['--check-template']:
        check_template()
    elif sys.argv[1:] == ['--self-test']:
        left, right = socket.socketpair()
        with left, right:
            left.sendall(packet(2, 0, 'Players connected (0):'))
            assert response(right) == (2, 0, 'Players connected (0):')
        for command, message in (('players', 'Players connected (0):'), ('save', 'World saved')):
            validate_reply(command, message)
            try:
                validate_reply(command, 'Unknown command')
            except RuntimeError:
                pass
            else:
                raise AssertionError('An error response passed validation')
        assert len(MAGIC) == 16
        print('Protocol framing and command-result checks passed')
    else:
        if len(sys.argv) != 5:
            raise SystemExit(__doc__)
        check(sys.argv[1], *map(int, sys.argv[2:]), os.environ['PZ_RCON_PASSWORD'])
