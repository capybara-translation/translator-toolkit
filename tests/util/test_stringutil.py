#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from translator_toolkit.util import stringutil


def test_unixtime_to_datetime():
    dt1 = datetime(2018, 2, 1, 12, 15, 30, 0000, tzinfo=timezone.utc)
    out1 = stringutil.unixtime_to_datetime(str(dt1.timestamp()), from_mxliff=False)
    assert out1 == dt1

    asia_tokyo = ZoneInfo('Asia/Tokyo')
    dt2 = datetime(2018, 2, 1, 12, 15, 30, 0000, tzinfo=asia_tokyo)
    out2 = stringutil.unixtime_to_datetime(str(dt2.timestamp()), tz=asia_tokyo, from_mxliff=False)
    assert out2 == dt2

    unix_from_mxliff = '1517487330000'
    out3 = stringutil.unixtime_to_datetime(unix_from_mxliff)
    dt3 = datetime(2018, 2, 1, 12, 15, 30, 0000, tzinfo=timezone.utc)
    assert out3 == dt3


def test_isoformat_to_datetime():
    s1 = '2020-04-05T15:57:58.6608253+09:00'
    out1 = stringutil.isoformat_to_datetime(s1)
    dt1 = datetime(2020, 4, 5, 15, 57, 58, 660825, tzinfo=timezone(timedelta(seconds=32400)))
    assert out1 == dt1
