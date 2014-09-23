from datetime import datetime as DT

from pytest import raises

from webhelpers2.date import distance_of_time_in_words as dtw
from webhelpers2.date import _is_leap_year

class TestDistanceOfTimeInWords(object):
    
    from_time = DT(2000, 1, 1, 0, 0, 0, 0, None) # Midnight, Jan 1 2000 UTC
    to_time = DT(1980, 5, 6, 12, 32, 40, 0, None) # 12:32pm, May 5, 1980

    def test_integer_seconds(self):
        # Test that if integers are supplied they are interpreted as seconds from now
        assert dtw(1) == "1 second"

    def test_now_to_1_year(self):

        # The following two tests test the span from "now" to "a year from
        # now".  Depending on when the test is run, the interval may include a
        # leap year.  The 'try' assumes it's not a leap year, the 'except'
        # tries it again as a leap year.
        try:
            assert dtw(0, 31536000) == "1 year"
            assert dtw(1, 31536001) == "1 year"
        except AssertionError:  # If the intervening year contains February 29th
            assert dtw(0, 31536000) == "11 months and 30 days" 
            assert dtw(1, 31536001) == "11 months and 30 days"
         
    def test_invalid_granularity(self):
        # Granularity is invalid
        raises(Exception, dtw, 0, 1, "blah")
        
    def test_february_nonleap(self):
        # February 2nd 2007 to March 1 2007 is 27 days because February is shorter month in the year
        assert dtw(DT(2007,2,2), DT(2007, 3, 1)) == "27 days"
        
    def test_february_leap(self):
        # February 2nd 2008 to March 1 2008 is 28 days because it's a leap year 
        assert dtw(DT(2008,2,2), DT(2008, 3, 1)) == "28 days"

    def test_symmetry(self):
        # Should get the same values going forward and backward
        from_time = self.from_time
        to_time = self.to_time
        assert dtw(from_time, to_time) == dtw(to_time, from_time)
        assert dtw(from_time, to_time, "month") ==  dtw(to_time, from_time, "month")
        assert dtw(from_time, to_time, "year") ==  dtw(to_time, from_time, "year")
        

    def test_granularity(self):
        # Ensure we get the correct granularity when the times are the same
        from_time = self.from_time
        assert dtw(from_time, from_time, "second") == "0 seconds"
        assert dtw(from_time, from_time, "day") == "0 days"
        assert dtw(from_time, from_time, "century") == "0 centuries"

    def test_smaller_than_granularity(self):
        # We are not over the finest granularity
        assert dtw(1, granularity="hour") == "less than 1 hour"
        assert dtw(86399, granularity="day") == "less than 1 day"
        
    def test_grandularity_round_up(self):
        # Round up if the granularity after the supplied granularity is high enough
        assert dtw(86399, round=True, granularity="day") == "1 day"
        assert dtw(290, round=True, granularity="minute") == "5 minutes"
        assert dtw(86689, round=True, granularity="minute") == "1 day and 5 minutes"
        
    def test_grandularity_round_second_value(self):
        # Rounding at the second value makes no difference
        from_time = self.from_time
        to_time = self.to_time
        assert dtw(to_time, from_time, granularity="second") == \
            dtw(to_time, from_time, granularity="second", round=True)
        
    def test_plural(self):
        # Pluralization
        assert dtw(DT(200, 1,1), DT(300, 1, 1)) == "1 century"
        assert dtw(DT(200, 1,1), DT(500, 1, 1)) == "3 centuries"
        
    def test_plural2(self):
        assert dtw(DT(2000, 1,1), DT(2000, 2, 1)) == "1 month"
        assert dtw(DT(2000, 1,1), DT(2000, 5, 1)) == "4 months"
        

class TestSpotChecks(object):
    def test_spot_checks(self):
        # Spot checks
        from_time = DT(200, 2, 2, 0, 12, 12, 0, None) # 12 minutes, 12 seconds past midnight on Feb 2 200AD
        to_time = DT(1981, 3, 31, 7, 31, 0, 0, None) # 7:31 am, March 31, 1981
        assert dtw(from_time, to_time) == "17 centuries, 8 decades, 1 year, 1 month, 29 days, 7 hours, 18 minutes and 48 seconds"
        assert dtw(from_time, to_time, granularity = "hour") == "17 centuries, 8 decades, 1 year, 1 month, 29 days and 7 hours"
        assert dtw(from_time, to_time, granularity = "hour", round=True) == "17 centuries, 8 decades, 1 year, 1 month, 29 days and 7 hours"
        assert dtw(from_time, to_time, granularity = "month") == "17 centuries, 8 decades, 1 year and 1 month"
        assert dtw(from_time, to_time, granularity = "month", round=True) == "17 centuries, 8 decades, 1 year and 2 months"
        
        from_time = DT(200, 2, 2, 12, 30, 30, 0, None) # 12:30:30, Feb 2, 200AD
        to_time = DT(220, 3, 2, 12, 30, 31, 0, None) # 12:30:31, Mar 2, 220AD
        assert dtw(from_time, to_time) == "2 decades, 1 month and 1 second"


class TestFormerDocTests(object):
    start = DT(2008,3,21, 16,34)
    end = DT(2008,2,6, 9,45)

    def test1(self):
        assert dtw(86399, round=True, granularity="day") == "1 day"

    def test2(self):
        assert dtw(86399, granularity='day') == "less than 1 day"

    def test3(self):
        assert dtw(86399) == "23 hours, 59 minutes and 59 seconds"

    def test4(self):
        b = "1 month, 15 days, 6 hours and 49 minutes"
        assert dtw(self.start, self.end) == b

    def test5(self):
        b = "less than 1 decade"
        assert dtw(self.start, self.end, granularity="decade") == b

    def test6(self):
        b = "1 month, 15 days, 6 hours and 49 minutes"
        assert dtw(self.start, self.end, granularity="second") == b


class TestLeapYears(object):
    def test_is_leap_year_1900(self):
        assert not _is_leap_year(1900)

    def test_is_leap_year_2000(self):
        assert _is_leap_year(2000)

    def test_is_leap_year_2011(self):
        assert not _is_leap_year(2011)

    def test_is_leap_year_2012(self):
        assert _is_leap_year(2012)

    def test_is_leap_year_2100(self):
        assert not _is_leap_year(2100)
