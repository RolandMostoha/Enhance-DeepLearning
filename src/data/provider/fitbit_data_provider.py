from datetime import date, timedelta
from typing import Dict, Any, Callable, Optional

from fitbit import Fitbit

from data.model.records import HeartRecord, BodyRecord, SleepRecord, ActivityRecord
from data.provider.data_provider import DataProvider
from utils.pager import pager


class FitbitDataProvider(DataProvider):

    def __init__(self, fitbit: Fitbit, start_date: date, end_date: date):
        self.fitbit = fitbit
        self.start_date = start_date
        self.end_date = end_date
        self.period_days = (end_date - start_date).days

    def get_heart_records(self) -> Dict[date, HeartRecord]:
        self.log_call('Heart')
        response = self.fitbit.time_series('activities/heart', base_date=self.start_date, end_date=self.end_date)
        heart_list = response['activities-heart']

        records: Dict[date, HeartRecord] = {}

        append_records(records, heart_list, 'dateTime', 'resting_heart', heart_rest_transformation)

        return records

    def get_body_records(self) -> Dict[date, BodyRecord]:
        self.log_call('Weight')
        response_weight = self.fitbit.time_series('body/weight', base_date=self.start_date, end_date=self.end_date)
        self.log_call('Fat')
        response_fat = self.fitbit.time_series('body/fat', base_date=self.start_date, end_date=self.end_date)
        self.log_call('BMI')
        response_bmi = self.fitbit.time_series('body/bmi', base_date=self.start_date, end_date=self.end_date)

        records: Dict[date, BodyRecord] = {}

        append_records(records, response_weight['body-weight'], 'dateTime', 'weight', body_value_transformation)
        append_records(records, response_fat['body-fat'], 'dateTime', 'fat', body_value_transformation)
        append_records(records, response_bmi['body-bmi'], 'dateTime', 'bmi', body_value_transformation)

        return records

    def get_sleep_records(self) -> Dict[date, SleepRecord]:
        records: Dict[date, SleepRecord] = {}

        response = pager(items_count=self.period_days, item_per_page=100, func=self.pager_sleep_records)

        append_records(records, response['sleep'], 'dateOfSleep', 'sleep_efficiency', sleep_efficiency_transformation)
        append_records(records, response['sleep'], 'dateOfSleep', 'sleep_duration', sleep_duration_transformation)

        return records

    def pager_sleep_records(self, start_index: int, end_index: int):
        start_date = self.start_date + timedelta(days=start_index)
        end_date = self.start_date + timedelta(days=end_index)
        self.log_call('Sleep', start_date, end_date)
        response = self.fitbit.time_series('sleep', base_date=start_date, end_date=end_date)
        return response

    def get_activity_records(self) -> Dict[date, ActivityRecord]:
        self.log_call('Calories')
        res_cal = self.fitbit.time_series('activities/calories', base_date=self.start_date, end_date=self.end_date)
        res_act_cal = pager(items_count=self.period_days, item_per_page=100, func=self.pager_active_calories)
        self.log_call('Sedentary minutes')
        res_min_sed = self.fitbit.time_series('activities/minutesSedentary', base_date=self.start_date,
                                              end_date=self.end_date)
        self.log_call('Lightly active minutes')
        res_min_light = self.fitbit.time_series('activities/minutesLightlyActive', base_date=self.start_date,
                                                end_date=self.end_date)
        self.log_call('Fairly active minutes')
        res_min_fair = self.fitbit.time_series('activities/minutesFairlyActive', base_date=self.start_date,
                                               end_date=self.end_date)
        self.log_call('Highly active minutes')
        res_min_very = self.fitbit.time_series('activities/minutesVeryActive', base_date=self.start_date,
                                               end_date=self.end_date)

        total_calories = res_cal['activities-calories']
        active_calories = res_act_cal['activities-activityCalories']
        sedentary_minutes = res_min_sed['activities-minutesSedentary']
        lightly_active_minutes = res_min_light['activities-minutesLightlyActive']
        fairly_active_minutes = res_min_fair['activities-minutesFairlyActive']
        highly_active_minutes = res_min_very['activities-minutesVeryActive']

        records: Dict[date, ActivityRecord] = {}

        append_records(records, total_calories, 'dateTime', 'total_calories', activity_transformation)
        append_records(records, active_calories, 'dateTime', 'active_calories', activity_transformation)
        append_records(records, sedentary_minutes, 'dateTime', 'sedentary_minutes', activity_transformation)
        append_records(records, lightly_active_minutes, 'dateTime', 'lightly_active_minutes', activity_transformation)
        append_records(records, fairly_active_minutes, 'dateTime', 'fairly_active_minutes', activity_transformation)
        append_records(records, highly_active_minutes, 'dateTime', 'highly_active_minutes', activity_transformation)

        return records

    def pager_active_calories(self, start_index: int, end_index: int):
        start_date = self.start_date + timedelta(days=start_index)
        end_date = self.start_date + timedelta(days=end_index)
        self.log_call('Active calories', start_date, end_date)
        response = self.fitbit.time_series('activities/activityCalories', base_date=start_date, end_date=end_date)
        return response

    def log_call(self, category: str, start_date: date = None, end_date: date = None):
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.end_date
        days = (end_date - start_date).days
        print("{} api call between {} -> {}(total days={})".format(category, start_date, end_date, days))


def append_records(records: Dict[date, Any],
                   response_list: list,
                   key_date: str,
                   key_record: str,
                   transform_record: Callable[[dict], Optional[Any]]):
    for record in response_list:
        record_date = date.fromisoformat(record[key_date])
        record_value = transform_record(record)

        if record_value is not None:
            if record_date not in records:
                records[record_date] = {}

            records[record_date][key_record] = record_value


def heart_rest_transformation(record_dict: dict) -> Optional[int]:
    if 'restingHeartRate' in record_dict['value']:
        return to_int(record_dict['value']['restingHeartRate'])
    else:
        return None


def body_value_transformation(record_dict: dict) -> float:
    return to_scaled_float(record_dict['value'])


def sleep_efficiency_transformation(record_dict: dict) -> int:
    return to_int(record_dict['efficiency'])


def activity_transformation(record_dict: dict) -> int:
    return to_int(record_dict['value'])


def sleep_duration_transformation(record_dict: dict) -> float:
    duration_ms = record_dict['duration']
    hours_scaled = format(float(duration_ms / (1000 * 60 * 60)), '.2f')
    return float(hours_scaled)


def to_scaled_float(value: str) -> float:
    value_scaled = format(float(value), '.2f')
    return float(value_scaled)


def to_int(value: str) -> int:
    return int(value)
