from pytest import raises

from webhelpers2.number import *

def eq(a, b, cutoff=0.001):
    """Assert that two floats are equal within 'cutoff' margin of error.
    """
    assert abs(a - b) < cutoff


class TestEQ(object):
    def test_good(self):
        eq(1.0001, 1.0002)

    def test_bad(self):
        with raises(AssertionError):
            eq(1.0, 2.0)

    def test_custom_cutoff(self):
        eq(2.0, 4.0, cutoff=3.0)


class TestPercentOf(object):
    def test1(self):
        assert percent_of(5, 100) == 5.0

    def test2(self):
        assert percent_of(13, 26) == 50.0


class TestMean(object):
    def test1(self):
        assert mean([5, 10]) == 7.5


class TestMedian(object):
    incomes = [18000, 24000, 32000, 44000, 67000, 9999999]

    def test_median(self):
        assert median(self.incomes) == 49500.0

    def test_compare_to_mean(self):
        eq(mean(self.incomes), 1697499.833333333)


class TestStandardDeviation(object):
    
    temps_socal = [  # Temperatures in Southern California.
      # Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
        70, 70, 70, 75, 80, 85, 90, 95, 90, 80, 75, 70]
    temps_mt = [   # Temperatures in Montana.
      # Jan  Feb  Mar Apr May Jun Jul  Aug Sep Oct Nov Dec
        -32, -10, 20, 30, 60, 90, 100, 80, 60, 30, 10, -32]

    def test1(self):
        a = standard_deviation([0, 0, 14, 14])
        eq(a, 8.082903768654761)

    def test2(self):
        a = standard_deviation([0, 6, 8, 14])
        eq(a, 5.773502691896258)

    def test3(self):
        a = standard_deviation([6, 6, 8, 8])
        eq(a, 1.1547005383792515)

    def test4(self):
        assert standard_deviation([0, 0, 14, 14], sample=False) == 7.0

    def test5(self):
        assert standard_deviation([0, 6, 8, 14], sample=False) == 5.0

    def test6(self):
        assert standard_deviation([6, 6, 8, 8], sample=False) == 1.0

    def test_temperatures_southern_california(self):
        a = standard_deviation(self.temps_socal)
        eq(a, 9.00336637385)
        
    def test_temperatures_southern_california2(self):
        a = standard_deviation(self.temps_socal, sample=False)
        eq(a, 8.620067027323)

    def test_temperatures_montana(self):
        a = standard_deviation(self.temps_mt)
        eq(a, 45.1378360405574)
        
    def test_temperatures_montana2(self):
        a = standard_deviation(self.temps_mt, sample=False)
        eq(a, 43.2161878106906)



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
