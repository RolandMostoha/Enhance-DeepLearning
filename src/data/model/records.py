from typing import TypedDict


class HeartRecord(TypedDict):
    resting_heart: int


class BodyRecord(TypedDict):
    weight: int
    fat: float
    bmi: float


HEART_RECORD_KEYS = list(HeartRecord.__annotations__.keys())

BODY_RECORD_KEYS = list(BodyRecord.__annotations__.keys())

RECORD_KEYS = HEART_RECORD_KEYS + BODY_RECORD_KEYS
