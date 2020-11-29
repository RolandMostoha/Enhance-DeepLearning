import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.python.keras.models import Sequential

from data.dataset_generator import DatasetGenerator
from plotter import plotter


class DNNTrainer:

    def __init__(self, dataset: DatasetGenerator, target_feature: str):
        self.target_feature = target_feature
        self.dataset = dataset

    def train(self) -> Sequential:
        dataset = self.dataset

        normalizer = preprocessing.Normalization()
        normalizer.adapt(np.array(dataset.x_train))

        model = tf.keras.models.Sequential([
            normalizer,
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(1, activation='linear')
        ], name="{}_tf_model".format(self.target_feature))

        model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.1),
            loss='mean_absolute_error'
        )
        model.build(dataset.x_train.shape)

        history = model.fit(
            dataset.x_train, dataset.y_train,
            epochs=200,
            validation_data=(dataset.x_valid, dataset.y_valid),
            verbose=0
        )
        plotter.plot_loss(self.target_feature, history)

        metrics = model.evaluate(dataset.x_test, dataset.y_test)
        print("{} x_test loss: {}".format(self.target_feature, metrics))

        return model
