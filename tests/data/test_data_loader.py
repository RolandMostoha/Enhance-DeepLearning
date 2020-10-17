import csv
import os
from datetime import date
from typing import Dict

import pytest
from pytest_mock import MockerFixture

from data.data_loader import DataLoader
from data.data_provider import DataProvider
from data.model.records import HeartRecord, BodyRecord


class MockDataProvider(DataProvider):

    def get_heart_records(self) -> Dict[date, HeartRecord]:
        pass

    def get_body_records(self) -> Dict[date, BodyRecord]:
        pass


class TestDataLoader:
    TEST_CSV_FILE = 'test_health_records.csv'

    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        data_provider = MockDataProvider()
        mock = mocker.patch.object(data_provider, 'get_heart_records')
        mock.return_value = {
            date(year=2020, month=1, day=1): {'resting_heart': 60}
        }
        mock = mocker.patch.object(data_provider, 'get_body_records')
        mock.return_value = {
            date(year=2020, month=1, day=1): {'weight': 75, 'fat': 15.12, 'bmi': 21.12},
            date(year=2020, month=1, day=2): {'weight': 74, 'fat': 14.12, 'bmi': 20.12}
        }

        self.data_loader = DataLoader(data_provider)

        yield self.data_loader

        if os.path.exists(self.TEST_CSV_FILE):
            os.remove(self.TEST_CSV_FILE)

    def test_generate_records(self):
        self.data_loader.generate_records()

        assert self.data_loader.records == {
            date(year=2020, month=1, day=1): {'resting_heart': 60, 'weight': 75, 'fat': 15.12, 'bmi': 21.12},
            date(year=2020, month=1, day=2): {'resting_heart': None, 'weight': 74, 'fat': 14.12, 'bmi': 20.12}
        }

    def test_write_to_csv(self):
        self.data_loader.generate_records()
        self.data_loader.write_to_csv("test_health_records.csv")

        with open(self.TEST_CSV_FILE, newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_first = next(reader)
            assert row_first == ['record_date', 'resting_heart', 'weight', 'fat', 'bmi']

            row_second = next(reader)
            assert row_second == ['2020-01-01', '60', '75', '15.12', '21.12']

            row_third = next(reader)
            assert row_third == ['2020-01-02', '', '74', '14.12', '20.12']
