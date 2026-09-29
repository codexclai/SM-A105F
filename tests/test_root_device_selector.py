import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class RootDeviceSelectorTests(unittest.TestCase):
    def test_explicit_root_selection_contract(self):
        result = subprocess.run(
            ["bash", str(ROOT / "tests/test_root_device_selector.sh")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("explicit selection validated", result.stdout)

    def test_init_and_resolver_are_posix_shell_syntax(self):
        for script in ("a105f-init", "root-device.sh"):
            subprocess.run(
                ["sh", "-n", str(ROOT / "configs/initramfs" / script)],
                check=True,
            )


if __name__ == "__main__":
    unittest.main()
