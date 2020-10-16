import abc
from datetime import date
from typing import List

from fitbit import Fitbit

from data.model.records import HeartRecord


class DataProvider(abc.ABC):

    @abc.abstractmethod
    def get_heart_records(self) -> List[HeartRecord]:
        pass


class FitbitDataProvider(DataProvider):

    def __init__(self, fitbit: Fitbit, start_date: date, end_date: date):
        self.fitbit = fitbit
        self.startDate = start_date
        self.endDate = end_date

    def get_heart_records(self) -> List[HeartRecord]:
        response = self.fitbit.time_series('activities/heart', base_date=self.startDate, end_date=self.endDate)

        heart_records: List[HeartRecord] = []

        for heart in response['activities-heart']:
            if 'restingHeartRate' in heart['value']:
                record_date = date.fromisoformat(heart['dateTime'])
                resting_heart = int(heart['value']['restingHeartRate'])
                heart_records.append({'record_date': record_date, 'resting_heart': resting_heart})

        return heart_records
