#!/usr/bin/env python3
"""MinIO template regression and real S3 checks (Python standard library).

python3 scripts/test_minio_images.py
MINIO_RUNTIME=1 python3 scripts/test_minio_images.py

Runtime checks require Docker and OpenSSL. They use isolated containers and
temporary data, certificates and credentials; no host ports are published.
MINIO_TEMPLATE_ROOT selects an unchanged fixture for a red run.
"""
import ast
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
import uuid

ROOT = Path(os.environ.get('MINIO_TEMPLATE_ROOT', Path(__file__).resolve().parents[1]))
CLIENTS = ('lobehub', 'litellm', 'coze-studio')
SERVERS = ('minio', 'tailchat', 'Reactive-Resume')
MARKERS = {'lobehub': 'wait-object-storage', 'litellm': 'init-s3-config', 'coze-studio': 'sync-storage-assets'}
SERVER_IMAGE = 'registry.cn-shenzhen.aliyuncs.com/teable/minio:RELEASE.2025-04-22T22-12-26Z@sha256:a1ea29fa28355559ef137d71fc570e508a214ec84ff8083e39bc5428980b015e'
CLIENT_IMAGE = 'registry.cn-shenzhen.aliyuncs.com/teable/minio-mc:RELEASE.2025-04-16T18-13-26Z@sha256:aead63c77f9db9107f1696fb08ecb0faeda23729cde94b0f663edf4fe09728e3'


def source(name):
    return (ROOT / 'template' / name / 'index.yaml').read_text()


def image(name):
    values = re.findall(r'^\s*image:\s*[\"\']?([^\"\'\s]+)', source(name), re.M)
    values = [value for value in values if '/minio' in value or value.startswith('minio/')]
    if len(values) != 1:
        raise AssertionError(f'{name}: expected one MinIO image, got {len(values)}')
    return values[0]


def client_script(name):
    text = source(name)
    if name == 'litellm':
        match = re.search(r'vn-tmpvn-initvn-s3vn-configvn-sh: \|\n((?:    [^\n]*\n|\n)+)', text)
    else:
        text = text.split('- name: ' + MARKERS[name] + '\n', 1)[1]
        match = re.search(r'- \|\n((?:              [^\n]*\n|\n)+)', text)
    if not match:
        raise AssertionError(f'{name}: shell block missing')
    return textwrap.dedent(match.group(1))


def yaml_list(text, field):
    match = re.search(r'^(\s*)' + field + r':\n((?:\s+- [^\n]+\n)+)', text, re.M)
    if not match:
        return None
    values = []
    for line in match.group(2).splitlines():
        value = line.strip()[2:]
        values.append(ast.literal_eval(value) if value[0] in '\"\'' else value)
    return values


def server_contract(name):
    text = source(name)
    pos = text.index('image: ' + image(name))
    block = text[pos:]
    if name == 'Reactive-Resume':
        match = re.search(r'command:\s*(\[[\s\S]*?\])', block)
        command = json.loads(match.group(1).replace(',\n            ]', '\n            ]'))
        args = []
    else:
        command = yaml_list(block, 'command')
        args = yaml_list(block, 'args')
    return {'template': name, 'image': image(name), 'command': command, 'args': args, 'user': '1000:1000' if name == 'Reactive-Resume' else None}


def contracts():
    return {'clients': [{'template': name, 'image': image(name), 'script': client_script(name)} for name in CLIENTS],
            'servers': [server_contract(name) for name in SERVERS]}


def run(*args, env=None, timeout=60):
    try:
        return subprocess.run(args, check=True, text=True, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout).stdout.strip()
    except subprocess.CalledProcessError as error:
        # 保留失败层证据，但不将临时测试凭据写入诊断输出。
        detail = error.stderr or ''
        for key in ('MINIO_ROOT_PASSWORD', 'S3_SECRET_ACCESS_KEY'):
            value = (env or {}).get(key)
            if value:
                detail = detail.replace(value, '[redacted]')
        print(detail, file=sys.stderr)
        raise


class SourceContract(unittest.TestCase):
    def test_all_six_images_are_available_pinned_candidates(self):
        for name in CLIENTS + SERVERS:
            with self.subTest(template=name):
                self.assertEqual(image(name), CLIENT_IMAGE if name in CLIENTS else SERVER_IMAGE)

    def test_displayed_server_image_matches_workload(self):
        for name in SERVERS:
            with self.subTest(template=name):
                values = re.findall(r'originImageName:\s*[\"\']?([^\"\'\s]+)', source(name))
                displayed = next(value for value in values if '/minio' in value)
                self.assertEqual(displayed, image(name))

    def test_runtime_contracts_are_read_from_templates(self):
        for name in CLIENTS:
            with self.subTest(template=name):
                self.assertIn('mc alias set', client_script(name))
        self.assertEqual(server_contract('minio')['args'][0], 'server')
        self.assertEqual(server_contract('tailchat')['command'], ['minio'])
        self.assertIn('/usr/bin/docker-entrypoint.sh', server_contract('Reactive-Resume')['command'][2])
        text = source('litellm')
        block = text[text.index("${{ if(inputs.enable_s3_storage === 'true') }}", text.index('kind: Deployment')):]
        self.assertLess(block.index('- name: init-s3-config'), block.index('${{ endif() }}'))


@unittest.skipUnless(os.environ.get('MINIO_RUNTIME') == '1', 'set MINIO_RUNTIME=1 for real S3 checks')
class S3Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix='minio-test-')
        cls.addClassCleanup(cls.directory.cleanup)
        cls.files = Path(cls.directory.name)
        cls.network = 'minio-test-' + uuid.uuid4().hex[:10]
        cls.env = dict(os.environ, MINIO_ROOT_USER='qa-user', MINIO_ROOT_PASSWORD=uuid.uuid4().hex,
                       S3_ACCESS_KEY_ID='qa-user', HOME='/tmp', MC_CONFIG_DIR='/tmp/.mc')
        cls.env['S3_SECRET_ACCESS_KEY'] = cls.env['MINIO_ROOT_PASSWORD']
        run('docker', 'network', 'create', cls.network)
        cls.addClassCleanup(run, 'docker', 'network', 'rm', cls.network)
        certs = cls.files / 'certs'
        certs.mkdir()
        run('openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-days', '1',
            '-subj', '/CN=s3.qa.test', '-addext', 'subjectAltName=DNS:s3.qa.test',
            '-keyout', str(certs / 'private.key'), '-out', str(certs / 'public.crt'))
        os.chmod(certs / 'private.key', 0o600)
        cls.backend = cls.network + '-s3'
        cls.start(cls.backend, SERVER_IMAGE, ['server', '/data', '--certs-dir', '/certs', '--console-address=:9001'],
                  aliases=['s3.qa.test'], mounts=[(certs, '/certs', True), (cls.data('s3'), '/data', False)])
        cls.wait('https://s3.qa.test:9000')
        cls.mc('https://s3.qa.test:9000', cls.mc_setup('https://s3.qa.test:9000') +
               'mc mb --ignore-existing qa/qa-bucket; mc stat qa/qa-bucket >/dev/null')

    @classmethod
    def data(cls, name):
        path = cls.files / name
        path.mkdir(exist_ok=True)
        path.chmod(0o777)
        return path

    @classmethod
    def start(cls, name, img, args, aliases=(), mounts=(), entrypoint=None, user=None, paused=False):
        command = ['docker', 'run', '-d', '--name', name, '--network', cls.network,
                   '-e', 'MINIO_ROOT_USER', '-e', 'MINIO_ROOT_PASSWORD']
        for alias in aliases:
            command += ['--network-alias', alias]
        for host, guest, readonly in mounts:
            command += ['-v', f'{host}:{guest}' + (':ro' if readonly else '')]
        if paused:
            original = [entrypoint] if entrypoint else json.loads(run('docker', 'image', 'inspect', img, '--format', '{{json .Config.Entrypoint}}'))
            command += ['--entrypoint', '/bin/sh']
            # 先注册所有节点的 DNS，再启动真实 MinIO；避免未注册名称回退宿主 fake-IP。
            args = ['-ec', 'while [ ! -f /tmp/qa-start-minio ]; do sleep 0.05; done; exec ' + shlex.join(original + args)]
        elif entrypoint:
            command += ['--entrypoint', entrypoint]
        if user:
            command += ['--user', user]
        run(*command, img, *args, env=cls.env)
        cls.addClassCleanup(run, 'docker', 'rm', '-f', name)

    @classmethod
    def release_distributed_nodes(cls, names, aliases):
        actual = {name: json.loads(run('docker', 'inspect', name))[0]['NetworkSettings']['Networks'][cls.network]['IPAddress'] for name in names}
        for source_node in names:
            for target, alias in zip(names, aliases):
                resolved = run('docker', 'exec', source_node, 'getent', 'ahostsv4', alias)
                addresses = {line.split()[0] for line in resolved.splitlines()}
                if addresses != {actual[target]}:
                    raise AssertionError('peer DNS does not resolve to its registered test container')
        for name in names:
            run('docker', 'exec', name, 'touch', '/tmp/qa-start-minio')

    @classmethod
    def mc(cls, endpoint, script, img=CLIENT_IMAGE, extra=None, mounts=(), user=None):
        environment = dict(cls.env, BACKEND_STORAGE_MINIO_EXTERNAL_ENDPOINT=endpoint.removeprefix('https://').removeprefix('http://'),
                           S3_BUCKET='qa-bucket', LITELLM_CONFIG_BUCKET_OBJECT_KEY='litellm_proxy_config.yaml',
                           SSL_CERT_FILE='/certs/public.crt')
        environment.update(extra or {})
        name = cls.network + '-client-' + uuid.uuid4().hex[:8]
        command = ['docker', 'run', '--rm', '--name', name, '--network', cls.network, '--entrypoint', '/bin/sh',
                   '-v', f'{cls.files / "certs"}:/certs:ro']
        for key in ('S3_ACCESS_KEY_ID', 'S3_SECRET_ACCESS_KEY', 'BACKEND_STORAGE_MINIO_EXTERNAL_ENDPOINT',
                    'S3_BUCKET', 'LITELLM_CONFIG_BUCKET_OBJECT_KEY', 'SSL_CERT_FILE', 'HOME', 'MC_CONFIG_DIR'):
            command += ['-e', key]
        for host, guest in mounts:
            command += ['-v', f'{host}:{guest}:ro']
        if user:
            command += ['--user', user]
        try:
            return run(*command, img, '-ec', script, env=environment, timeout=45)
        finally:
            # docker CLI 超时不会自动终止容器，必须清理本次具名测试容器。
            subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @classmethod
    def mc_setup(cls, endpoint):
        return f'mc alias set qa {endpoint} "$S3_ACCESS_KEY_ID" "$S3_SECRET_ACCESS_KEY" >/dev/null; '

    @classmethod
    def wait(cls, endpoint):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            try:
                cls.mc(endpoint, cls.mc_setup(endpoint) + 'mc ready qa >/dev/null')
                return
            except subprocess.CalledProcessError:
                time.sleep(0.5)
        raise AssertionError('isolated MinIO did not become ready')

    @classmethod
    def wait_distributed_initialization(cls, names):
        # 官方 server-main 先暴露健康状态，再异步初始化配置子系统。
        # 测试等待当前进程的明确完成事件，不用固定延迟或重试写入掩盖初始化竞争。
        starts = {name: run('docker', 'inspect', '--format', '{{.State.StartedAt}}', name) for name in names}
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            # MinIO 生命周期日志走 stderr，docker logs 的两个输出流都属于证据。
            logs = [subprocess.run(['docker', 'logs', '--since', starts[name], name],
                                   check=True, text=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, timeout=30).stdout for name in names]
            if all('All MinIO sub-systems initialized successfully' in text for text in logs):
                return
            time.sleep(0.2)
        raise AssertionError('four current MinIO processes did not finish subsystem initialization')

    def test_required_shell_tools_and_binary_versions(self):
        out = run('docker', 'run', '--rm', '--entrypoint', '/bin/sh', CLIENT_IMAGE, '-ec',
                  'mc --version; command -v seq; command -v sleep')
        self.assertIn('RELEASE.2025-04-16T18-13-26Z', out)
        out = run('docker', 'run', '--rm', SERVER_IMAGE, '--version')
        self.assertIn('RELEASE.2025-04-22T22-12-26Z', out)

    def test_three_actual_client_scripts_over_verified_https(self):
        endpoint = 'https://s3.qa.test:9000'
        self.mc(endpoint, client_script('lobehub'), img=image('lobehub'), user='65534:65534')
        self.mc(endpoint, client_script('litellm'), img=image('litellm'))
        uploaded = self.mc(endpoint, self.mc_setup(endpoint) + 'mc cat qa/qa-bucket/litellm_proxy_config.yaml')
        self.assertIn('model_list: []', uploaded)
        # 已有配置不能被重复初始化覆盖；通过真实对象内容检验。
        self.mc(endpoint, self.mc_setup(endpoint) + "printf 'existing-config' | mc pipe qa/qa-bucket/litellm_proxy_config.yaml >/dev/null")
        self.mc(endpoint, client_script('litellm'), img=image('litellm'))
        self.assertEqual(self.mc(endpoint, self.mc_setup(endpoint) + 'mc cat qa/qa-bucket/litellm_proxy_config.yaml'), 'existing-config')
        work = self.data('work')
        for directory in ('default_icon', 'official_plugin_icon'):
            path = work / 'repo/docker/volumes/minio' / directory
            path.mkdir(parents=True)
            (path / 'qa.txt').write_text(directory + '-content')
        self.mc(endpoint, client_script('coze-studio'), img=image('coze-studio'), mounts=[(work, '/work')])
        for directory in ('default_icon', 'official_plugin_icon'):
            actual = self.mc(endpoint, self.mc_setup(endpoint) + f'mc cat qa/qa-bucket/{directory}/qa.txt')
            self.assertEqual(actual, directory + '-content')

    def exercise_storage(self, endpoint, bucket):
        setup = self.mc_setup(endpoint)
        self.mc(endpoint, setup + f'mc mb qa/{bucket}; printf "persisted-object" | mc pipe qa/{bucket}/qa.txt >/dev/null')
        self.assertEqual(self.mc(endpoint, setup + f'mc cat qa/{bucket}/qa.txt'), 'persisted-object')
        with self.assertRaises(subprocess.CalledProcessError):
            self.mc(endpoint, setup + f'mc stat qa/{bucket}/qa.txt', extra={'S3_SECRET_ACCESS_KEY': uuid.uuid4().hex})
        self.mc(endpoint, setup + f'mc anonymous set download qa/{bucket}')
        self.assertIn('download', self.mc(endpoint, setup + f'mc anonymous get qa/{bucket}'))

    def test_two_single_node_server_commands_and_restart_persistence(self):
        for name in ('tailchat', 'Reactive-Resume'):
            with self.subTest(template=name):
                contract = server_contract(name)
                container = self.network + '-' + name.lower()
                command = contract['command']
                self.start(container, contract['image'], command[1:] + contract['args'],
                           entrypoint=command[0], user=contract['user'], mounts=[(self.data(name), '/data', False)])
                endpoint = f'http://{container}:9000'
                self.wait(endpoint)
                self.exercise_storage(endpoint, 'qa-data')
                if name == 'Reactive-Resume':
                    console = run('docker', 'exec', container, 'curl', '-fsS', 'http://localhost:9001/')
                    self.assertIn('<html', console.lower())
                    self.assertGreater(len(console), 500)
                run('docker', 'restart', container)
                self.wait(endpoint)
                self.assertEqual(self.mc(endpoint, self.mc_setup(endpoint) + 'mc cat qa/qa-data/qa.txt'), 'persisted-object')

    def test_four_node_distributed_template_and_restart_persistence(self):
        contract = server_contract('minio')
        app = self.network + '-distributed'
        args = [value.replace('${{ defaults.app_name }}', app).replace('${{ SEALOS_NAMESPACE }}', 'qa') for value in contract['args']]
        names = []
        aliases = []
        for i in range(4):
            name = app + '-' + str(i)
            names.append(name)
            alias = f'{name}.{app}.qa.svc.cluster.local'
            aliases.append(alias)
            volume = name + '-data'
            run('docker', 'volume', 'create', volume)
            self.addClassCleanup(run, 'docker', 'volume', 'rm', volume)
            self.start(name, contract['image'], args, aliases=[alias],
                       mounts=[(volume, '/data', False)], paused=True)
        self.release_distributed_nodes(names, aliases)
        endpoint = f'http://{names[0]}:9000'
        self.wait(endpoint)
        self.wait_distributed_initialization(names)
        self.exercise_storage(endpoint, 'qa-data')
        console = run('docker', 'exec', names[0], 'curl', '-fsS', 'http://localhost:9001/')
        self.assertIn('<html', console.lower())
        run('docker', 'restart', *names)
        self.wait(endpoint)
        self.wait_distributed_initialization(names)
        self.assertEqual(self.mc(endpoint, self.mc_setup(endpoint) + 'mc cat qa/qa-data/qa.txt'), 'persisted-object')


if __name__ == '__main__':
    if sys.argv[1:] == ['--contracts']:
        print(json.dumps(contracts()))
    else:
        unittest.main(verbosity=2)
