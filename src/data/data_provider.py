import abc
from datetime import date
from typing import Dict, Any

from fitbit import Fitbit

from data.model.records import HeartRecord, BodyRecord


class DataProvider(abc.ABC):

    @abc.abstractmethod
    def get_heart_records(self) -> Dict[date, HeartRecord]:
        pass

    @abc.abstractmethod
    def get_body_records(self) -> Dict[date, BodyRecord]:
        pass


class FitbitDataProvider(DataProvider):

    def __init__(self, fitbit: Fitbit, start_date: date, end_date: date):
        self.fitbit = fitbit
        self.startDate = start_date
        self.endDate = end_date

    def get_heart_records(self) -> Dict[date, HeartRecord]:
        response = self.fitbit.time_series('activities/heart', base_date=self.startDate, end_date=self.endDate)

        heart_records: Dict[date, HeartRecord] = {}

        for heart in response['activities-heart']:
            if 'restingHeartRate' in heart['value']:
                record_date = date.fromisoformat(heart['dateTime'])
                resting_heart = int(heart['value']['restingHeartRate'])

                heart_records[record_date] = {'resting_heart': resting_heart}

        return heart_records

    def get_body_records(self) -> Dict[date, BodyRecord]:
        response_weight = self.fitbit.time_series('body/weight', base_date=self.startDate, end_date=self.endDate)
        response_fat = self.fitbit.time_series('body/fat', base_date=self.startDate, end_date=self.endDate)
        response_bmi = self.fitbit.time_series('body/bmi', base_date=self.startDate, end_date=self.endDate)

        body_records: Dict[date, BodyRecord] = {}

        append_records(body_records, response_weight['body-weight'], 'weight')
        append_records(body_records, response_fat['body-fat'], 'fat')
        append_records(body_records, response_bmi['body-bmi'], 'bmi')

        return body_records


def append_records(records: Dict[date, Any], response: list, key: str):
    for record in response:
        record_date = date.fromisoformat(record['dateTime'])

        if record_date not in records:
            records[record_date] = {}

        records[record_date][key] = record['value']
