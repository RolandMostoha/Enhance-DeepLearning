from datetime import date

from fitbit import Fitbit


class DataLoader:
    def __init__(self, fitbit: Fitbit, start_date: date, end_date: date):
        self.fitbit = fitbit
        self.endDate = end_date
        self.startDate = start_date

    def generate_resting_heart(self) -> dict:
        response_json = self.fitbit.time_series('activities/heart', base_date=self.startDate, end_date=self.endDate)

        heart_list = response_json['activities-heart']

        heart_dict = {}
        for heart in heart_list:
            if 'restingHeartRate' in heart['value']:
                record_date = heart['dateTime']
                resting_heart_rate = heart['value']['restingHeartRate']
                heart_dict[record_date] = resting_heart_rate

        return heart_dict
