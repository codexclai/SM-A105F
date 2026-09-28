import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKER = ROOT / "scripts/build_android_dt_table.py"


def minimal_fdt():
    structure = struct.pack(">I", 1) + bytes(4) + struct.pack(">II", 2, 9)
    total = 40 + 16 + len(structure)
    header = struct.pack(">10I", 0xD00DFEED, total, 56, total, 40, 17, 16, 0, 0, len(structure))
    return header + bytes(16) + structure


class AndroidDtTableBuilderTests(unittest.TestCase):
    def test_wraps_one_fdt_in_page_aligned_v0_table(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "test.dtb"
            image = Path(tmp) / "dt.img"
            expected = minimal_fdt()
            raw.write_bytes(expected)
            subprocess.run([sys.executable, str(PACKER), str(raw), str(image), "--id", "0x1234", "--rev", "2", "--custom", "1", "2", "3", "4"], check=True)
            data = image.read_bytes()
        header = struct.unpack_from(">8I", data)
        magic, total, header_size, entry_size, count, entries_offset, page_size, version = header
        self.assertEqual((magic, header_size, entry_size, count, entries_offset, page_size, version), (0xD7B7AB1E, 32, 32, 1, 32, 2048, 0))
        self.assertEqual(total, len(data))
        size, offset, ident, revision, *custom = struct.unpack_from(">8I", data, entries_offset)
        self.assertEqual(offset, 2048)
        self.assertEqual((ident, revision, custom), (0x1234, 2, [1, 2, 3, 4]))
        self.assertEqual(data[offset:offset + size], expected)
        self.assertEqual(len(data) % page_size, 0)

    def test_rejects_invalid_fdt_structure_bounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw = Path(tmp) / "bad.dtb"
            image = Path(tmp) / "dt.img"
            damaged = bytearray(minimal_fdt())
            struct.pack_into(">I", damaged, 8, len(damaged) + 4)
            raw.write_bytes(damaged)
            result = subprocess.run([sys.executable, str(PACKER), str(raw), str(image)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("input FDT is invalid", result.stderr)


if __name__ == "__main__":
    unittest.main()
