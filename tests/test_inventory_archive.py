import importlib.util
import io
import pathlib
import tarfile
import tempfile
import unittest
import zipfile


SOURCE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "inventory-archive.py"
spec = importlib.util.spec_from_file_location("inventory_archive", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class InventoryArchiveTest(unittest.TestCase):
    def test_tar_warns_about_traversal_and_does_not_extract(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            path = root / "AP_example.tar"
            with tarfile.open(path, "w") as archive:
                payload = b"stock fixture"
                member = tarfile.TarInfo("../escape.img")
                member.size = len(payload)
                archive.addfile(member, io.BytesIO(payload))
            data = module.inventory(path)
            self.assertEqual(data["format"], "tar")
            self.assertEqual(data["members"][0]["size_bytes"], len(payload))
            self.assertTrue(any("Unsafe member" in message for message in data["warnings"]))
            self.assertFalse((root.parent / "escape.img").exists())

    def test_zip_lists_members_without_claiming_payload_integrity(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "firmware.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("BL_example.tar.md5", b"fixture")
            data = module.inventory(path)
            self.assertEqual(data["format"], "zip")
            self.assertEqual(data["members"][0]["name"], "BL_example.tar.md5")
            self.assertIn("crc32_claimed", data["members"][0])


if __name__ == "__main__":
    unittest.main()
