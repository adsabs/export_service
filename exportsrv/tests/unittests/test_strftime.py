# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import datetime

import exportsrv.app as app
from exportsrv.formatter.strftime import strftime


class TestExports(TestCase):

    def create_app(self):
        app_ = app.create_app()
        return app_

    # Make sure that the day names are in order
    # from 1/1/1 until August 2000
    def test_strftime(self):
        s = strftime(datetime.date(1800, 9, 23),
                     "%Y has the same days as 1980 and 2008")
        assert(s == "1800 has the same days as 1980 and 2008")

        # Get the weekdays.  Can't hard code them; they could be localized.
        days = []
        for i in range(1, 10):
            days.append(datetime.date(2000, 1, i).strftime("%A"))
        nextday = {}
        for i in range(8):
            nextday[days[i]] = days[i+1]
        assert(days == ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        assert(nextday == {'Monday': 'Tuesday', 'Tuesday': 'Wednesday', 'Friday': 'Saturday', 'Wednesday': 'Thursday', 'Thursday': 'Friday', 'Sunday': 'Monday', 'Saturday': 'Sunday'})

        # Testing all day names from 0001/01/01 until 2000/08/01
        startdate = datetime.date(1, 1, 1)
        enddate = datetime.date(2000, 8, 1)
        prevday = strftime(startdate, "%A")
        one_day = datetime.timedelta(1)
        assert(prevday == 'Monday')

        # Testing century
        testdate = startdate + one_day
        while testdate < enddate:
            day = strftime(testdate, "%A")
            assert(nextday[prevday] == day)
            prevday = day
            testdate = testdate + one_day

if __name__ == '__main__':
  unittest.main()
