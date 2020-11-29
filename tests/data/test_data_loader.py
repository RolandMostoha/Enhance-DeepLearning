import csv
import os
from datetime import date
from typing import Dict

import pytest
from pytest_mock import MockerFixture

from data.data_loader import DataLoader
from data.model.records import HeartRecord, BodyRecord, SleepRecord, ActivityRecord
from data.provider.data_provider import DataProvider


class MockDataProvider(DataProvider):

    def get_heart_records(self) -> Dict[date, HeartRecord]:
        pass

    def get_body_records(self) -> Dict[date, BodyRecord]:
        pass

    def get_sleep_records(self) -> Dict[date, SleepRecord]:
        pass

    def get_activity_records(self) -> Dict[date, ActivityRecord]:
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
        mock = mocker.patch.object(data_provider, 'get_sleep_records')
        mock.return_value = {
            date(year=2020, month=1, day=1): {'sleep_duration': 480, 'sleep_efficiency': 80}
        }
        mock = mocker.patch.object(data_provider, 'get_activity_records')
        mock.return_value = {
            date(year=2020, month=1, day=2): {'total_calories': 1600,
                                              'active_calories': 400,
                                              'sedentary_minutes': 600,
                                              'lightly_active_minutes': 10,
                                              'fairly_active_minutes': 10,
                                              'highly_active_minutes': 10}
        }

        self.data_loader = DataLoader(data_provider)

        yield self.data_loader

        if os.path.exists(self.TEST_CSV_FILE):
            os.remove(self.TEST_CSV_FILE)

    def test_generate_records(self):
        self.data_loader.generate_records()

        assert self.data_loader.records == {
            date(year=2020, month=1, day=1): {'resting_heart': 60,
                                              'weight': 75,
                                              'fat': 15.12,
                                              'bmi': 21.12,
                                              'sleep_duration': 480,
                                              'sleep_efficiency': 80,
                                              'total_calories': None,
                                              'active_calories': None,
                                              'sedentary_minutes': None,
                                              'lightly_active_minutes': None,
                                              'fairly_active_minutes': None,
                                              'highly_active_minutes': None},
            date(year=2020, month=1, day=2): {'resting_heart': None,
                                              'weight': 74,
                                              'fat': 14.12,
                                              'bmi': 20.12,
                                              'sleep_duration': None,
                                              'sleep_efficiency': None,
                                              'total_calories': 1600,
                                              'active_calories': 400,
                                              'sedentary_minutes': 600,
                                              'lightly_active_minutes': 10,
                                              'fairly_active_minutes': 10,
                                              'highly_active_minutes': 10}
        }

    def test_write_to_csv(self):
        self.data_loader.generate_records()
        self.data_loader.write_to_csv("test_health_records.csv")

        with open(self.TEST_CSV_FILE, newline='') as csv_file:
            reader = csv.reader(csv_file)
            row_first = next(reader)
            assert row_first == ['record_date',
                                 'resting_heart',
                                 'weight',
                                 'fat',
                                 'bmi',
                                 'sleep_duration',
                                 'sleep_efficiency',
                                 'total_calories',
                                 'active_calories',
                                 'sedentary_minutes',
                                 'lightly_active_minutes',
                                 'fairly_active_minutes',
                                 'highly_active_minutes']

            row_second = next(reader)
            assert row_second == ['2020-01-01', '60', '75', '15.12', '21.12', '480', '80', '', '', '', '', '', '']

            row_third = next(reader)
            assert row_third == ['2020-01-02', '', '74', '14.12', '20.12', '', '', '1600', '400', '600', '10', '10',
                                 '10']
