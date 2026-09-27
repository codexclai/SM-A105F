

import struct
import unittest

from scripts.inspect_android_boot_layout import parse_boot_header, parse_dt_table


class BootLayoutParserTests(unittest.TestCase):
    def test_v1_boot_header_reports_empty_ramdisk(self):
        data = bytearray(2048)
        data[:8] = b"ANDROID!"
        struct.pack_into("<10I", data, 8,
                         0x1000, 0x10008000, 0, 0, 0, 0,
                         0x10000100, 2048, 1, 0)
        data[48:64] = b"SRPSA10A009KU\0"
        struct.pack_into("<I", data, 1632, 0)
        struct.pack_into("<Q", data, 1636, 0)
        struct.pack_into("<I", data, 1644, 1648)
        result = parse_boot_header(bytes(data))
        self.assertEqual(result["header_version"], 1)
        self.assertEqual(result["kernel_load_address"], 0x10008000)
        self.assertEqual(result["ramdisk_size"], 0)
        self.assertEqual(result["product_name"], "SRPSA10A009KU")

    def test_boot_header_rejects_bad_magic(self):
        with self.assertRaisesRegex(ValueError, "Android boot image"):
            parse_boot_header(b"NOTBOOT!" + bytes(2040))

    def test_dt_table_rejects_bad_magic(self):
        with self.assertRaisesRegex(ValueError, "DT table"):
            parse_dt_table(bytes(64))

    def test_dt_table_decodes_single_fdt_compatible(self):
        compatible = b"samsung,A10 SWA OPEN 00\0"
        strings = b"compatible\0"
        structure = (struct.pack(">I", 1) + bytes(4) +
                     struct.pack(">III", 3, len(compatible), 0) + compatible +
                     bytes((-len(compatible)) % 4) + struct.pack(">II", 2, 9))
        struct_off = 56
        strings_off = struct_off + len(structure)
        total_fdt = strings_off + len(strings)
        fdt = (struct.pack(">10I", 0xD00DFEED, total_fdt, struct_off,
                           strings_off, 40, 17, 16, 0, len(strings), len(structure)) +
               bytes(16) + structure + strings)
        offset = 64
        total = offset + len(fdt)
        table = (struct.pack(">8I", 0xD7B7AB1E, total, 32, 32, 1,
                             32, 2048, 0) +
                 struct.pack(">8I", len(fdt), offset, 0, 0, 0, 255, 0, 0) + fdt)
        result = parse_dt_table(table)
        self.assertEqual(result["entry_count"], 1)
        self.assertEqual(result["entries"][0]["fdt"]["compatible"],
                         ["samsung,A10 SWA OPEN 00"])


if __name__ == "__main__":
    unittest.main()

