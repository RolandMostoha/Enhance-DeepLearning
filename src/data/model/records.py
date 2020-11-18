from typing import TypedDict


class HeartRecord(TypedDict):
    resting_heart: int


class BodyRecord(TypedDict):
    weight: int
    fat: float
    bmi: float


class SleepRecord(TypedDict):
    sleep_duration: int
    sleep_efficiency: int


KEYS_HEART = list(HeartRecord.__annotations__.keys())

KEYS_BODY = list(BodyRecord.__annotations__.keys())

KEYS_SLEEP = list(SleepRecord.__annotations__.keys())

KEYS_HEALTH_RECORDS = KEYS_HEART + KEYS_BODY + KEYS_SLEEP
