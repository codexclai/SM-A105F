import hashlib
import struct
import unittest

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


if __name__ == "__main__":
    unittest.main()
