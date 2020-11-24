from datetime import date
from typing import OrderedDict

import matplotlib.pyplot as plt
from tensorflow.python.keras.callbacks import History

from data.model.records import KEYS_ALL_HEALTH_RECORDS


def plot_records(health_records: OrderedDict[date, dict]):
    fig, axs = plt.subplots(len(KEYS_ALL_HEALTH_RECORDS))
    fig.suptitle('Health Records')

    for key in KEYS_ALL_HEALTH_RECORDS:
        records = []
        dates = []
        for record_date, record in health_records.items():
            dates.append(record_date)
            records.append(record[key])

        axs[KEYS_ALL_HEALTH_RECORDS.index(key)].plot(dates, records)
        axs[KEYS_ALL_HEALTH_RECORDS.index(key)].set(ylabel=key)

    fig.autofmt_xdate()
    plt.show()


def plot_loss(feature: str, history: History):
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Error: {}'.format(feature))
    plt.legend()
    plt.grid(True)
    plt.show()
