import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.extract_android_boot_sections import extract


def make_v1(kernel=b"KERNEL!", ramdisk=b"RAMDISK"):
    page = 2048
    image = bytearray(page)
    image[:8] = b"ANDROID!"
    struct.pack_into("<10I", image, 8,
                     len(kernel), 0x10008000, len(ramdisk), 0x11000000,
                     0, 0, 0x10000100, page, 1, 0)
    image[1632:1648] = struct.pack("<IQI", 0, 0, 1648)
    image.extend(kernel)
    image.extend(bytes((-len(kernel)) % page))
    image.extend(ramdisk)
    image.extend(bytes((-len(ramdisk)) % page))
    return bytes(image)


class BootSectionExtractionTests(unittest.TestCase):
    def test_extracts_kernel_and_ramdisk_at_aligned_offsets(self):
        image = make_v1()
        manifest, payloads = extract(image)
        self.assertEqual(payloads, {"kernel": b"KERNEL!", "ramdisk": b"RAMDISK"})
        self.assertEqual(manifest["sections"]["kernel"]["offset"], 2048)
        self.assertEqual(manifest["sections"]["ramdisk"]["offset"], 4096)
        self.assertEqual(manifest["sections"]["ramdisk"]["sha256"],
                         hashlib.sha256(b"RAMDISK").hexdigest())

    def test_rejects_truncated_kernel_payload(self):
        with self.assertRaisesRegex(ValueError, "kernel section"):
            extract(make_v1()[:2048 + 3])

    def test_rejects_non_v1_header(self):
        data = bytearray(make_v1())
        struct.pack_into("<I", data, 8 + 8 * 4, 0)
        with self.assertRaisesRegex(ValueError, "only Android boot header v1"):
            extract(bytes(data))

    def test_cli_writes_round_trip_payloads_and_hash_manifest(self):
        root = Path(__file__).resolve().parents[1]
        tool = root / "scripts" / "extract_android_boot_sections.py"
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            boot, kernel, ramdisk, output = (tmp / "boot.img", tmp / "Image",
                                              tmp / "initramfs.cpio.gz", tmp / "out")
            boot.write_bytes(make_v1())
            kernel.write_bytes(b"KERNEL!")
            ramdisk.write_bytes(b"RAMDISK")
            result = subprocess.run(
                [sys.executable, str(tool), str(boot), str(output),
                 "--expected-kernel", str(kernel), "--expected-ramdisk", str(ramdisk)],
                check=True, capture_output=True, text=True)
            self.assertEqual((output / "kernel.bin").read_bytes(), kernel.read_bytes())
            self.assertEqual((output / "ramdisk.bin").read_bytes(), ramdisk.read_bytes())
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["sections"]["kernel"]["sha256"],
                             hashlib.sha256(kernel.read_bytes()).hexdigest())
            self.assertEqual(json.loads(result.stdout), manifest)


if __name__ == "__main__":
    unittest.main()
