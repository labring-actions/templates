"""Check port allocation and native game readiness with Python and PyYAML.

Usage: python3 scripts/test_7daystodie_template.py
"""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import MagicMock, patch

import yaml


template = Path(__file__).resolve().parents[1] / 'template/7daystodie/index.yaml'
documents = list(yaml.safe_load_all(template.read_text()))
config = next(document for document in documents if document['kind'] == 'ConfigMap')
service = next(document for document in documents if document['kind'] == 'Service')
workload = next(document for document in documents if document['kind'] == 'StatefulSet')
role = next(document for document in documents if document['kind'] == 'Role')
app_name = workload['metadata']['name']
service_name = app_name + '-nodeport'
assert service['metadata']['name'] == service_name
assert workload['spec']['serviceName'] == service_name
assert role['rules'][0]['resourceNames'] == [service_name]
assert service['metadata']['labels']['app'] == app_name
assert service['spec']['selector']['app'] == app_name
assert service['spec']['type'] == 'ClusterIP'
initializer = workload['spec']['template']['spec']['initContainers'][0]
assert {'name': 'SERVICE_NAME', 'value': service_name} in initializer['env']
print('Dedicated NodePort Service references and atomic initialization contract passed')
source = config['data']['vn-etcvn-sealosvn-runtimevn-py']
compile(source, 'runtime.py', 'exec')
with tempfile.TemporaryDirectory() as directory:
    script = Path(directory) / 'runtime.py'
    script.write_text(source)
    subprocess.run([sys.executable, str(script), '--self-test'], check=True)
    runtime = {'__name__': 'template_runtime'}
    exec(compile(source, 'runtime.py', 'exec'), runtime)
    runtime['SAVES'] = Path(directory)
    (Path(directory) / '.sealos-port').write_text('31000')
    cases = [
        ([b'01', b'946\r\nGameType:7', b'DTD;\r\nLevelName:Navezgane;\r\n'], bytes([14]), True),
        ([b''], bytes([14]), False),
        ([b'GameType:Other;\r\n', b''], bytes([14]), False),
        ([b'GameType:7DTD;\r\nLevelName:Navezgane;\r\n'], bytes([0]), False),
    ]
    for chunks, udp_response, expected in cases:
        tcp = MagicMock()
        tcp.__enter__.return_value = tcp
        tcp.recv.side_effect = chunks
        udp = MagicMock()
        udp.__enter__.return_value = udp
        udp.recv.return_value = udp_response
        with patch.object(runtime['socket'], 'create_connection', return_value=tcp), \
                patch.object(runtime['socket'], 'socket', return_value=udp), \
                redirect_stdout(StringIO()):
            try:
                runtime['query']()
                actual = True
            except RuntimeError:
                actual = False
        assert actual == expected, 'Unexpected readiness result'
        if expected:
            udp.connect.assert_called_once_with(('127.0.0.1', 31002))
            udp.send.assert_called_once_with(bytes([3, 0, 0]))
    print('Fragmented TCP, empty/invalid responses and LiteNetLib checks passed')

    account = MagicMock()
    account.__truediv__.side_effect = lambda name: MagicMock(
        read_text=lambda: {'namespace': 'test', 'token': 'test-token'}[name])
    selected = runtime['ports'](31000)
    reset_targets = [dict(port, targetPort=port['port']) for port in selected]
    high_ports = [dict(port, nodePort=port['nodePort'] + 5000) for port in selected]
    for initial, expected_base, patch_count in [
            (selected, 31000, 0), (reset_targets, 31000, 1),
            (high_ports, 31234, 1)]:
        updates = []

        def open_service(request, **kwargs):
            assert request.full_url.endswith('/namespaces/test/services/test-nodeport')
            if request.get_method() == 'PATCH':
                updates.append(json.loads(request.data))
            return StringIO(json.dumps({'metadata': {'resourceVersion': '1'},
                                        'spec': {'ports': initial}}))

        with patch.dict(runtime['os'].environ, {'SERVICE_NAME': 'test-nodeport'}), \
                patch.dict(runtime, {'Path': lambda path: account}), \
                patch.object(runtime['ssl'], 'create_default_context'), \
                patch.object(runtime['urllib'].request, 'urlopen', side_effect=open_service), \
                patch.object(runtime['os'], 'chown'), \
                patch.object(runtime['secrets'], 'randbelow', return_value=1234), \
                redirect_stdout(StringIO()):
            runtime['allocate']()
        assert (Path(directory) / '.sealos-port').read_text() == str(expected_base)
        assert len(updates) == patch_count, 'Unexpected Service patch count'
        if updates:
            assert updates[0]['spec']['ports'] == runtime['ports'](expected_base)
            assert updates[0]['metadata']['resourceVersion'] == '1'
    print('Existing port reuse, target-port repair and out-of-range allocation checks passed')
