#!/usr/bin/env python3

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = "81ea0b4779f70ad4a4fc2b08da302cd2317ad066682f448a611a530c681844e6"


def normalized_header(header):
	text = header.read_text(encoding="utf-8")
	text, substitutions = re.subn(
		r"^// Generated .* UTC$",
		"// Generated <normalized> UTC",
		text,
		count=1,
		flags=re.MULTILINE,
	)
	if substitutions != 1:
		raise ValueError("single header has no unique generation timestamp")
	return text.encode("utf-8")


def generate_header(temp_dir, name):
	temp_dir = Path(temp_dir)
	fake_bin = temp_dir / "bin"
	fake_bin.mkdir(exist_ok=True)
	fake_git = fake_bin / "git"
	fake_git.write_text(
		"#!/usr/bin/env python3\n"
		"import sys\n"
		"commands = {\n"
		"    ('rev-parse', '--short', 'HEAD'): '2b0d2fe8',\n"
		"    ('describe', '--tags', '--abbrev=0'): 'v3.3.1',\n"
		"}\n"
		"try:\n"
		"    print(commands[tuple(sys.argv[1:])])\n"
		"except KeyError:\n"
		"    raise SystemExit(2)\n",
		encoding="utf-8",
	)
	fake_git.chmod(0o755)
	output_dir = temp_dir / name
	output_dir.mkdir()
	environment = os.environ.copy()
	environment["PATH"] = str(fake_bin) + os.pathsep + environment["PATH"]
	subprocess.run(
		[
			"python3",
			str(ROOT / "single" / "single.py"),
			"--quiet",
			"--output",
			str(output_dir / "sol.hpp"),
			str(output_dir / "forward.hpp"),
			str(output_dir / "config.hpp"),
		],
		cwd=ROOT,
		env=environment,
		check=True,
	)
	return output_dir / "sol.hpp"


class SingleHeaderSnapshotTests(unittest.TestCase):
	def test_amalgamation_matches_admitted_snapshot(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			first = normalized_header(generate_header(temp_dir, "first"))
			second = normalized_header(generate_header(temp_dir, "second"))
			self.assertEqual(first, second)
			self.assertEqual(hashlib.sha256(first).hexdigest(), EXPECTED_SHA256)

	def test_modified_snapshot_is_rejected(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			header = normalized_header(generate_header(temp_dir, "negative"))
			modified = header + b"\n"
			self.assertNotEqual(hashlib.sha256(modified).hexdigest(), EXPECTED_SHA256)


if __name__ == "__main__":
	unittest.main(verbosity=2)
