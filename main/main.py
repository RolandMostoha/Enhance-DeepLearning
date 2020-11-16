def main():
    from auth.fitbit_authenticator import FitbitAuthenticator
    from datetime import timedelta
    from fitbit import Fitbit
    from data.data_loader import DataLoader
    from data.provider.fitbit_data_provider import FitbitDataProvider
    import tensorflow as tf
    import pandas as pd
    import numpy as np
    import fitbit as fitbit
    from datetime import date
    from plotter import plotter
    from tensorflow.keras import layers
    from tensorflow.keras.layers.experimental import preprocessing

    from data.dataset_generator import DatasetGenerator

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

    dataset = DatasetGenerator(data_frame, target_feature='fat')
    dataset.split(train_ratio=0.75, valid_ratio=0.15, test_ratio=0.10)

    tf.keras.backend.clear_session()
    tf.random.set_seed(60)

    normalizer = preprocessing.Normalization()
    normalizer.adapt(np.array(dataset.x_train))

    model = tf.keras.models.Sequential([
        normalizer,
        layers.Dense(units=1),
    ], name="LinearRegression")

    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.1),
        loss='mean_absolute_error',
        metrics=['mean_absolute_error']
    )
    model.build(dataset.x_train.shape)
    print(model.summary())

    history = model.fit(
        dataset.x_train, dataset.y_train,
        epochs=50,
        validation_data=(dataset.x_valid, dataset.y_valid),
        verbose=0
    )
    plotter.plot_loss(history)

    test_input = np.array([[65, 70, 24, 32340000, 80]])
    print(test_input, '\n Shape:', test_input.shape, end='\n')

    predictions = model.predict(dataset.x_test)
    print(predictions)

    metrics = model.evaluate(dataset.x_test, dataset.y_test)
    print("Test loss, accuracy:", metrics)


if __name__ == '__main__':
    main()
