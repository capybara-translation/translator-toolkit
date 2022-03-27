#!/usr/bin/env python3
from typing import Optional
from datetime import datetime, timezone, tzinfo
import regex


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def unixtime_to_datetime(value: str, tz: tzinfo = timezone.utc, from_mxliff: bool = True) -> datetime:
    if from_mxliff:
        return datetime.fromtimestamp(float(value) / 1000, tz) if is_float(value) else datetime.fromtimestamp(0, tz)
    return datetime.fromtimestamp(float(value), tz) if is_float(value) else datetime.fromtimestamp(0, tz)


def isoformat_to_datetime(value: str) -> Optional[datetime]:
    m = regex.search(r'(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.(?P<ms>\d{1,})(?P<offset>\+.+)', value)
    if not m:
        return None
    ms = m.group('ms')[:6]
    new_value = f'{m.group("datetime")}.{ms}{m.group("offset")}'
    return datetime.fromisoformat(new_value)
