import random
from datetime import date, timedelta
from typing import Dict

from data.model.records import ActivityRecord, SleepRecord, BodyRecord, HeartRecord, KEYS_HEART, KEYS_BODY, KEYS_SLEEP, \
    KEYS_ACTIVITIES
from data.provider.data_provider import DataProvider


class RandomDataProvider(DataProvider):

    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date
        self.random_ranges = {
            'resting_heart': (50, 70),
            'weight': (70, 100),
            'bmi': (20, 80),
            'fat': (10, 30),
            'sleep_duration': (300, 540),
            'sleep_efficiency': (50, 100),
            'total_calories': (1000, 3000),
            'active_calories': (0, 2000),
            'sedentary_minutes': (400, 800),
            'lightly_active_minutes': (0, 120),
            'fairly_active_minutes': (0, 60),
            'highly_active_minutes': (0, 120)
        }

    def get_heart_records(self) -> Dict[date, HeartRecord]:
        return self.__generate_random_record(KEYS_HEART)

    def get_body_records(self) -> Dict[date, BodyRecord]:
        return self.__generate_random_record(KEYS_BODY)

    def get_sleep_records(self) -> Dict[date, SleepRecord]:
        return self.__generate_random_record(KEYS_SLEEP)

    def get_activity_records(self) -> Dict[date, ActivityRecord]:
        return self.__generate_random_record(KEYS_ACTIVITIES)

    def __generate_random_record(self, keys):
        records = {}

        for day_index in range((self.end_date - self.start_date).days):
            record = {}
            for key in keys:
                value = random.randint(self.random_ranges[key][0], self.random_ranges[key][1])
                record[key] = value

            records[self.start_date + timedelta(days=day_index)] = record

        return records
