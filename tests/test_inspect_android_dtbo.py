import struct
import unittest

from scripts.inspect_android_dtbo import DtboError, inspect_dtbo


def make_table(*, page_size: int = 2048, dt_offset: int = 64) -> bytes:
    entry_size = 32
    entries_offset = 32
    payload = struct.pack(">I", 0xD00DFEED) + b"test-fdt"
    total_size = dt_offset + len(payload)
    header = struct.pack(">8I", 0xD7B7AB1E, total_size, 32, entry_size,
                         1, entries_offset, page_size, 0)
    entry = struct.pack(">8I", len(payload), dt_offset, 0x12, 0x34,
                        0x56, 0x78, 0x9A, 0xBC)
    return header + entry + bytes(dt_offset - len(header) - len(entry)) + payload


class InspectDtboTests(unittest.TestCase):
    def test_reads_v0_header_and_board_metadata(self):
        result = inspect_dtbo(make_table())
        self.assertEqual(result["magic"], "0xd7b7ab1e")
        self.assertEqual(result["page_size"], 2048)
        self.assertEqual(result["version"], 0)
        self.assertEqual(result["entries"][0]["id"], 0x12)
        self.assertEqual(result["entries"][0]["custom"], [0x56, 0x78, 0x9A, 0xBC])

    def test_rejects_non_dtbo_magic(self):
        with self.assertRaisesRegex(DtboError, "bad DT table magic"):
            inspect_dtbo(b"\0" * 40)

    def test_rejects_entry_outside_table(self):
        data = bytearray(make_table(dt_offset=0x1000))
        struct.pack_into(">I", data, 4, 64)
        with self.assertRaisesRegex(DtboError, "outside the declared table bounds"):
            inspect_dtbo(bytes(data))

    def test_rejects_invalid_page_size(self):
        with self.assertRaisesRegex(DtboError, "power of two"):
            inspect_dtbo(make_table(page_size=3000))

    def test_rejects_non_fdt_payload(self):
        data = bytearray(make_table())
        data[64:68] = b"NOPE"
        with self.assertRaisesRegex(DtboError, "FDT magic"):
            inspect_dtbo(bytes(data))


if __name__ == "__main__":
    unittest.main()
