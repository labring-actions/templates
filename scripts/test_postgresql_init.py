#!/usr/bin/env python3
"""Regression checks for the eight PostgreSQL initialization Jobs.

python3 scripts/test_postgresql_init.py
PG_INIT_RUNTIME=1 python3 scripts/test_postgresql_init.py

Runtime mode requires Docker and executes the actual template scripts against
an isolated PostgreSQL 14.8 container. No host ports or real credentials are used.
PG_INIT_TEMPLATE_ROOT can point to an unchanged checkout for a red run.
"""

import os
from pathlib import Path
import re
import subprocess
import textwrap
import time
import unittest
import uuid

ROOT = Path(os.environ.get("PG_INIT_TEMPLATE_ROOT", Path(__file__).resolve().parents[1]))
NAMES = ("glitchtip", "halo", "plane", "refly", "teable", "tianji", "tolgee", "mindoc")
RUNTIME = os.environ.get("PG_INIT_RUNTIME") == "1"


def init_container(name):
    """Read the literal image and shell block, without evaluating template expressions."""
    source = (ROOT / "template" / name / "index.yaml").read_text()
    container = source.split("- name: pgsql-init\n", 1)[1]
    image = re.search(r"^\s+image: (\S+)\s*$", container, re.MULTILINE).group(1)
    command = re.search(
        r"command:\n\s+- /bin/sh\n\s+- -c\n\s+- \|\n((?:[ ]{14}[^\n]*\n)+)",
        container,
    )
    if command is None:
        raise AssertionError(f"{name}: expected explicit /bin/sh -c literal script")
    return image, textwrap.dedent(command.group(1))


def docker(*args, timeout=30):
    return subprocess.run(
        ["docker", *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
    ).stdout.strip()


class TemplateContract(unittest.TestCase):
    def test_client_images_are_public_versioned_and_immutable(self):
        images = []
        for name in NAMES:
            with self.subTest(template=name):
                image, _ = init_container(name)
                self.assertRegex(
                    image,
                    r"^docker\.io/library/postgres:14\.[0-9]+-alpine3\.[0-9]+@sha256:[0-9a-f]{64}$",
                )
                images.append(image)
        self.assertEqual(len(set(images)), 1)

    def test_shell_preserves_url_as_one_argument(self):
        for name in NAMES:
            with self.subTest(template=name):
                _, script = init_container(name)
                self.assertIn('"${DATABASE_URL}"', script)
                self.assertNotIn("&>", script)


@unittest.skipUnless(RUNTIME, "set PG_INIT_RUNTIME=1 for real Docker/SQL checks")
class RuntimeContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.network = "pg-init-test-" + uuid.uuid4().hex[:10]
        cls.server = cls.network + "-db"
        docker("network", "create", cls.network)
        cls.addClassCleanup(docker, "network", "rm", cls.network)
        docker(
            "run", "-d", "--name", cls.server, "--network", cls.network,
            "--network-alias", "pg", "-e", "POSTGRES_HOST_AUTH_METHOD=trust",
            "docker.io/library/postgres:14.8-alpine",
        )
        cls.addClassCleanup(docker, "rm", "-f", cls.server)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                docker("exec", cls.server, "pg_isready", "-U", "postgres")
                break
            except subprocess.CalledProcessError:
                time.sleep(0.2)
        else:
            raise AssertionError("isolated PostgreSQL 14.8 did not become ready")

    def test_required_tools(self):
        image, _ = init_container("plane")
        output = docker(
            "run", "--rm", "--entrypoint", "/bin/sh", image, "-ec",
            "psql --version; pg_isready --version; command -v grep; command -v sleep",
        )
        self.assertIn("PostgreSQL) 14.", output)

    def test_all_actual_scripts_create_their_database(self):
        for name in NAMES:
            with self.subTest(template=name):
                image, script = init_container(name)
                docker(
                    "run", "--rm", "--network", self.network,
                    "--entrypoint", "/bin/sh", "-e",
                    "DATABASE_URL=postgresql://postgres@pg:5432/postgres",
                    image, "-c", script, timeout=20,
                )
                actual = docker(
                    "exec", self.server, "psql", "-U", "postgres", "-d", "postgres",
                    "-tAc", f"SELECT datname FROM pg_database WHERE datname='{name}'",
                )
                self.assertEqual(actual, name)

    def test_shell_waits_for_sql_and_keeps_url_intact(self):
        # 使用慢 psql 替身验证 shell 不会把 SQL 后台化；真实 SQL 另由上一测试覆盖。
        prelude = """
psql() {
  [ "$1" = "$DATABASE_URL" ] || return 22
  sleep 0.2
  touch /tmp/sql-complete
  printf '1\\n'
}
pg_isready() { return 0; }
"""
        for name in NAMES:
            with self.subTest(template=name):
                image, script = init_container(name)
                docker(
                    "run", "--rm", "--entrypoint", "/bin/sh", "-e",
                    "DATABASE_URL=connection with spaces", image, "-c",
                    prelude + script + '\n[ -f /tmp/sql-complete ]', timeout=10,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
