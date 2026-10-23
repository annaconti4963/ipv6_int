import unittest

from ipv6_int import ipv6_to_int, int_to_ipv6, IPv6FormatError


class TestIpv6ToInt(unittest.TestCase):

    def test_full_form(self):
        self.assertEqual(
            ipv6_to_int("2001:0db8:0000:0000:0000:0000:0000:0001"),
            0x20010DB8000000000000000000000001,
        )

    def test_double_colon_shorthand(self):
        self.assertEqual(ipv6_to_int("2001:db8::1"), 0x20010DB8000000000000000000000001)

    def test_loopback(self):
        self.assertEqual(ipv6_to_int("::1"), 1)

    def test_unspecified(self):
        self.assertEqual(ipv6_to_int("::"), 0)

    def test_uppercase_hex(self):
        self.assertEqual(ipv6_to_int("2001:DB8::ABCD"), 0x20010DB800000000000000000000ABCD)

    def test_embedded_ipv4(self):
        self.assertEqual(
            ipv6_to_int("::ffff:192.0.2.1"),
            0x00000000000000000000FFFFC0000201,
        )

    def test_empty_string(self):
        with self.assertRaises(IPv6FormatError):
            ipv6_to_int("")

    def test_triple_colon(self):
        with self.assertRaises(IPv6FormatError):
            ipv6_to_int("2001:::1")

    def test_too_many_groups(self):
        with self.assertRaises(IPv6FormatError):
            ipv6_to_int("1:2:3:4:5:6:7:8:9")

    def test_garbage_text(self):
        with self.assertRaises(IPv6FormatError):
            ipv6_to_int("not-an-address")

    def test_ipv4_not_embedded(self):
        with self.assertRaises(IPv6FormatError):
            ipv6_to_int("192.0.2.1")


class TestIntToIpv6(unittest.TestCase):

    def test_one(self):
        self.assertEqual(int_to_ipv6(1), "::1")

    def test_zero(self):
        self.assertEqual(int_to_ipv6(0), "::")

    def test_compresses_longest_run(self):
        self.assertEqual(
            int_to_ipv6(0x20010DB8000000000000000000000001),
            "2001:db8::1",
        )

    def test_no_compression_when_no_zero_run(self):
        self.assertEqual(
            int_to_ipv6(0x20010DB8112233445566778899AABBCC),
            "2001:db8:1122:3344:5566:7788:99aa:bbcc",
        )

    def test_negative_rejected(self):
        with self.assertRaises(IPv6FormatError):
            int_to_ipv6(-1)

    def test_overflow_rejected(self):
        with self.assertRaises(IPv6FormatError):
            int_to_ipv6(1 << 128)

    def test_non_int_rejected(self):
        with self.assertRaises(IPv6FormatError):
            int_to_ipv6("2001:db8::1")  # type: ignore[arg-type]


class TestRoundTrip(unittest.TestCase):

    def test_roundtrip(self):
        for text in ["::1", "::", "2001:db8::1", "fe80::1234:5678:9abc:def0"]:
            self.assertEqual(int_to_ipv6(ipv6_to_int(text)), text)


if __name__ == "__main__":
    unittest.main()
