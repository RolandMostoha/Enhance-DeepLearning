import csv
from datetime import date
from typing import Dict

from data.data_provider import DataProvider
from data.model.records import HeartRecord, RecordBase


class DataLoader:

    def __init__(self, data_provider: DataProvider):
        self.data_provider = data_provider
        self.records: Dict[date, dict] = {}

    def generate_records(self):
        heart_records = self.data_provider.get_heart_records()
        for heart_record in heart_records:
            record_date = heart_record['record_date']

            self.records[record_date] = {
                'resting_heart': heart_record['resting_heart']
            }

    def write_to_csv(self, file: str):
        headers = create_headers()

        with open(file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(headers)

            for record_date, record in self.records.items():
                writer.writerow([record_date] + list(record.values()))


def create_headers():
    headers_record_base = list(RecordBase.__annotations__.keys())

    header_heart = list(HeartRecord.__annotations__.keys())
    for header in headers_record_base:
        header_heart.remove(header)

    return headers_record_base + header_heart
