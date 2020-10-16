from datetime import date
from typing import TypedDict


class RecordBase(TypedDict):
    record_date: date


class HeartRecord(RecordBase, total=False):
    resting_heart: int
