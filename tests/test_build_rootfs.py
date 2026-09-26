"""Regression checks for build-rootfs.sh output-path safety.

These tests stop at the early path guards, before external build prerequisites
or Debian network access are needed.
"""
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-rootfs.sh"


class RootfsOutputSafetyTests(unittest.TestCase):
    def run_builder(self, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), str(output)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_refuses_existing_archive_without_modifying_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "rootfs.tar"
            output.write_bytes(b"keep existing archive")
            result = self.run_builder(output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("Refusing to overwrite", result.stderr)
            self.assertEqual(output.read_bytes(), b"keep existing archive")
            self.assertFalse(Path(f"{output}.sha256").exists())

    def test_refuses_existing_checksum_without_overwriting_or_building(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "rootfs.tar"
            checksum = Path(f"{output}.sha256")
            checksum.write_text("keep existing checksum\n")
            result = self.run_builder(output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("checksum", result.stderr)
            self.assertEqual(checksum.read_text(), "keep existing checksum\n")
            self.assertFalse(output.exists())

    def test_refuses_dangling_archive_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "rootfs.tar"
            output.symlink_to(Path(temp) / "missing-target")
            result = self.run_builder(output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertTrue(output.is_symlink())

    def test_refuses_dangling_checksum_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "rootfs.tar"
            checksum = Path(f"{output}.sha256")
            checksum.symlink_to(Path(temp) / "missing-target")
            result = self.run_builder(output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertTrue(checksum.is_symlink())
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
