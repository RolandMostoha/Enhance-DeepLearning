from fitbit import Fitbit

from data.fitbit_data_provider import FitbitDataProvider


def main():
    from datetime import date, timedelta

    import fitbit as fitbit

    from src.auth.fitbit_authenticator import FitbitAuthenticator
    from src.data.data_loader import DataLoader

    auth = FitbitAuthenticator("../configs/fitbit_auth_config.json")
    auth.authenticate_in_browser()

    fitbit = fitbit.Fitbit(auth.client_id, auth.client_secret,
                           access_token=auth.access_token,
                           refresh_token=auth.refresh_token,
                           system=Fitbit.METRIC)

    start_date = date(year=2020, month=1, day=1)
    end_date = date.today() - timedelta(days=1)

    data_provider = FitbitDataProvider(fitbit, start_date, end_date)

    loader = DataLoader(data_provider)
    loader.generate_records()

    loader.write_to_csv("../data/raw/health_records.csv")


if __name__ == '__main__':
    main()
