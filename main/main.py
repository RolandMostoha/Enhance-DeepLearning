def main():
    from data.model.records import KEYS_HEALTH_RECORDS
    from trainer.trainer import Trainer
    from auth.fitbit_authenticator import FitbitAuthenticator
    from datetime import timedelta
    from fitbit import Fitbit
    from data.data_loader import DataLoader
    from data.provider.fitbit_data_provider import FitbitDataProvider
    import fitbit as fitbit
    from datetime import date
    import pandas as pd

    from plotter import plotter

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

    plotter.plot_records(loader.records)

    loader.write_to_csv("../data/raw/health_records.csv")

    data_frame = pd.read_csv("../data/raw/health_records.csv")
    data_frame = data_frame.fillna(data_frame.mean())
    data_frame = data_frame.drop(columns=['record_date'])

    pd.set_option('display.max_columns', 15)

    last_record = data_frame.tail(1)
    print('Last health record:\n', last_record)

    # Update the desired values for my personal goal
    my_goal = last_record.copy()
    my_goal['weight'] = 65
    print('My personal goal:\n', my_goal)

    my_goal_prediction = ''

    keys = KEYS_HEALTH_RECORDS

    for key in keys:
        trainer = Trainer(data_frame, key)

        model = trainer.train()

        # Drop the target feature that we are train for
        my_goal_input = my_goal.drop(columns=[key])

        prediction = model.predict(my_goal_input)

        feature_prediction = 'Predicted {} value for the desired goal: {}'.format(key, prediction)
        my_goal_prediction += '\n' + feature_prediction

    print(my_goal_prediction)


if __name__ == '__main__':
    main()
