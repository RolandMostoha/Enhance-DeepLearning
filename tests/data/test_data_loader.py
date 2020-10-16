import csv
import os
from datetime import date
from typing import List

import pytest
from pytest_mock import MockerFixture

from data.data_loader import DataLoader
from data.data_provider import DataProvider
from data.model.records import HeartRecord


class MockDataProvider(DataProvider):

    def get_heart_records(self) -> List[HeartRecord]:
        pass


class TestDataLoader:
    test_csv_file = 'test_health_records.csv'

    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        data_provider = MockDataProvider()
        mock = mocker.patch.object(data_provider, 'get_heart_records')
        mock.return_value = [
            {'record_date': date(year=2020, month=1, day=1), 'resting_heart': 60},
            {'record_date': date(year=2020, month=1, day=2), 'resting_heart': 62}
        ]
        self.data_loader = DataLoader(data_provider)

        yield self.data_loader

        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_generate_records(self):
        self.data_loader.generate_records()

        assert self.data_loader.records == {
            date(year=2020, month=1, day=1): {'resting_heart': 60},
            date(year=2020, month=1, day=2): {'resting_heart': 62}
        }

    def test_write_to_csv(self):
        self.data_loader.generate_records()
        self.data_loader.write_to_csv("test_health_records.csv")

        with open(self.test_csv_file, newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_first = next(reader)
            assert row_first == ['record_date', 'resting_heart']

            row_second = next(reader)
            assert row_second == ['2020-01-01', '60']
