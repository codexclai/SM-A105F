import unittest

from scripts.audit_systemd_kernel_config import audit_config, parse_config


class SystemdKernelConfigAuditTests(unittest.TestCase):
    def test_parses_enabled_modules_and_unset_symbols(self):
        values = parse_config('CONFIG_FHANDLE=y\nCONFIG_IPV6=m\n# CONFIG_USER_NS is not set\n')
        self.assertEqual(values["CONFIG_FHANDLE"], "y")
        self.assertEqual(values["CONFIG_IPV6"], "m")
        self.assertEqual(values["CONFIG_USER_NS"], "n")

    def test_required_options_pass_but_sandbox_gaps_are_explicit(self):
        values = {name: "y" for name in (
            "CONFIG_DEVTMPFS", "CONFIG_CGROUPS", "CONFIG_INOTIFY_USER",
            "CONFIG_SIGNALFD", "CONFIG_TIMERFD", "CONFIG_EPOLL", "CONFIG_UNIX",
            "CONFIG_NET", "CONFIG_SYSFS", "CONFIG_PROC_FS", "CONFIG_FHANDLE")}
        values.update({"CONFIG_NET_NS": "n", "CONFIG_USER_NS": "n"})
        result = audit_config(values)
        self.assertTrue(result["core_requirements_pass"])
        self.assertEqual(result["service_sandbox_gaps"], ["CONFIG_NET_NS", "CONFIG_USER_NS"])

    def test_missing_core_and_user_firmware_loader_are_reported(self):
        values = {name: "y" for name in (
            "CONFIG_DEVTMPFS", "CONFIG_CGROUPS", "CONFIG_INOTIFY_USER",
            "CONFIG_SIGNALFD", "CONFIG_TIMERFD", "CONFIG_EPOLL", "CONFIG_UNIX",
            "CONFIG_NET", "CONFIG_SYSFS", "CONFIG_PROC_FS", "CONFIG_FHANDLE")}
        values["CONFIG_FW_LOADER_USER_HELPER"] = "y"
        del values["CONFIG_FHANDLE"]
        result = audit_config(values)
        self.assertFalse(result["core_requirements_pass"])
        self.assertEqual(result["core_missing"], ["CONFIG_FHANDLE"])
        self.assertEqual(result["required_disabled_options_enabled"],
                         ["CONFIG_FW_LOADER_USER_HELPER"])

    def test_nonempty_legacy_uevent_helper_is_reported(self):
        result = audit_config({"CONFIG_UEVENT_HELPER_PATH": "/sbin/hotplug"})
        self.assertEqual(result["legacy_hotplug_helpers_configured"],
                         ["CONFIG_UEVENT_HELPER_PATH"])


if __name__ == "__main__":
    unittest.main()
