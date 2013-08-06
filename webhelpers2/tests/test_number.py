from webhelpers2.number import *

class TestFormatDataSize(object):
    def test_bytes(self):
        assert format_byte_size(1) ==  "1 B"

    def test_kibibytes(self):
        assert format_byte_size(1000, binary=True) ==  "1000 B"
        assert format_byte_size(1024, 0, True) ==  "1 KiB"
        assert format_byte_size(1024, 2, True) ==  "1.00 KiB"

    def test_kilobytes(self):
        assert format_byte_size(1000),  "1.0 kB"
        assert format_byte_size(1024, 0, False) ==  "1 kB"
        assert format_byte_size(1024, 2, False) ==  "1.02 kB"
        assert format_byte_size(1024, 0, False, True) ==  "1 kilobytes"
        assert format_byte_size(1024, 2, False, True) ==  "1.02 kilobytes"

    def test_kilobits(self):
        assert format_bit_size(1024, 0, False, False) ==  "1 kb"
        assert format_bit_size(1024, 2, False, False) ==  "1.02 kb"
        assert format_bit_size(1024, 0, False, True) ==  "1 kilobits"
        assert format_bit_size(1024, 2, False, True) ==  "1.02 kilobits"

    def test_megabytes(self):
        assert format_byte_size(12345678, 2, True) ==  "11.77 MiB"
        assert format_byte_size(12345678, 2, False) ==  "12.35 MB"

    def test_terabytes(self):
        assert format_byte_size(12345678901234, 2, True) ==  "11.23 TiB"
        assert format_byte_size(12345678901234, 2, False) ==  "12.35 TB"

    def test_zettabytes(self):
        assert format_byte_size(1234567890123456789012, 2, True) ==  "1.05 ZiB"
        assert format_byte_size(1234567890123456789012, 2, False) ==  "1.23 ZB"

    def test_yottabytes(self):
        assert format_byte_size(123456789012345678901234567890, 2, True) == "102121.06 YiB"
        assert format_byte_size(123456789012345678901234567890, 2, False) ==  "123456.79 YB"
