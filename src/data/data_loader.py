import csv
from collections import OrderedDict
from datetime import date
from typing import Dict, Any, List

from data.model.records import KEYS_ALL_HEALTH_RECORDS, KEYS_HEART, KEYS_BODY, KEYS_SLEEP, KEYS_ACTIVITIES
from data.provider.data_provider import DataProvider


class DataLoader:

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.records: OrderedDict[date, dict] = OrderedDict()

    def generate_records(self):
        heart_records = self.data_provider.get_heart_records()
        body_records = self.data_provider.get_body_records()
        sleep_records = self.data_provider.get_sleep_records()
        activity_records = self.data_provider.get_activity_records()

        self.__append_records(heart_records, KEYS_HEART)
        self.__append_records(body_records, KEYS_BODY)
        self.__append_records(sleep_records, KEYS_SLEEP)
        self.__append_records(activity_records, KEYS_ACTIVITIES)
        self.__fill_empties_with_none()
        self.__sort_by_date()

    def __append_records(self, records: Dict[date, Any], record_keys: List[str]):
        for record_date, record in records.items():
            if record_date not in self.records:
                self.records[record_date] = {}

            for key in record_keys:
                self.records[record_date][key] = record[key]

    def __fill_empties_with_none(self):
        for record_date, record in self.records.items():
            for key in KEYS_ALL_HEALTH_RECORDS:
                if key not in record.keys():
                    record[key] = None

    def __sort_by_date(self):
        self.records = OrderedDict(sorted(self.records.items(), key=lambda x: x[0]))

    def write_to_csv(self, file: str):
        headers = ['record_date'] + KEYS_HEART + KEYS_BODY + KEYS_SLEEP + KEYS_ACTIVITIES

        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

            for record_date, record in self.records.items():
                ordered_records = []
                for record_key in KEYS_ALL_HEALTH_RECORDS:
                    ordered_records.append(record[record_key])

                writer.writerow([record_date] + ordered_records)
