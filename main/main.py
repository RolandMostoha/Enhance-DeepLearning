def main():
    from data.model.records import KEYS_ALL_HEALTH_RECORDS
    from trainer.linear_regression_trainer import LinearRegressionTrainer
    from auth.fitbit_authenticator import FitbitAuthenticator
    from datetime import timedelta
    from fitbit import Fitbit
    from data.data_loader import DataLoader
    from data.provider.fitbit_data_provider import FitbitDataProvider
    import fitbit as fitbit
    from datetime import date
    import pandas as pd
    import tensorflow as tf
    import seaborn as seaborn
    from data.dataset_generator import DatasetGenerator

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

    plotter.plot_all_records(loader.records)

    loader.write_to_csv("../data/raw/health_records.csv")

    # Initial setup
    pd.set_option('display.max_columns', 15)
    tf.keras.backend.clear_session()
    tf.random.set_seed(60)

    data_frame = pd.read_csv("../data/raw/health_records.csv")
    data_frame = data_frame.fillna(data_frame.mean())
    data_frame = data_frame.drop(columns=['record_date'])

    # Find correlations manually
    seaborn.pairplot(data_frame[KEYS_ALL_HEALTH_RECORDS], diag_kind='kde')

    # Check dataset stats
    print(data_frame.describe().transpose())

    last_record = data_frame.tail(1)
    print('Most recent health record:\n', last_record)

    # Set the modified values for my personal goal
    my_goal_changes = {'weight': 65}

    # Merging the most recent record with the modified values
    my_goal = last_record.copy()
    for key, value in my_goal_changes.items():
        my_goal[key] = value
    print('My goal merged with most recent health record:\n', my_goal)

    record_keys = KEYS_ALL_HEALTH_RECORDS

    # Skip the modified ones, there is no need to predict overwritten records
    for key in my_goal_changes.keys():
        record_keys.remove(key)

    prediction_results = 'Results for my goal {}'.format(my_goal_changes)

    for key in record_keys:
        dataset = DatasetGenerator(data_frame, target_feature=key)
        dataset.split(train_ratio=0.75, valid_ratio=0.15, test_ratio=0.10)

        trainer = LinearRegressionTrainer(dataset, key)

        model = trainer.train()

        # Drop the target feature that we are train for
        my_goal_input = my_goal.drop(columns=[key])

        prediction = model.predict(my_goal_input)

        feature_prediction = 'Predicted {} value for my goal: {}'.format(key, prediction)
        prediction_results += '\n' + feature_prediction

    print(prediction_results)


if __name__ == '__main__':
    main()
