from datetime import date
from typing import OrderedDict, Dict

import matplotlib.pyplot as plt
from tensorflow.python.keras.callbacks import History


def plot_all_records(health_records: OrderedDict[date, dict]):
    fig_labels_basic = {
        'resting_heart': 'rest_heart',
        'weight': 'weight',
        'fat': 'fat',
        'bmi': 'bmi',
        'sleep_duration': 'sleep_dur',
        'sleep_efficiency': 'sleep_eff'
    }
    plot_records(health_records, fig_labels_basic)
    fig_labels_activities = {
        'total_calories': 'cal_tot',
        'active_calories': 'cal_act',
        'sedentary_minutes': 'min_sed',
        'lightly_active_minutes': 'min_li',
        'fairly_active_minutes': 'min_fair',
        'highly_active_minutes': 'min_high'
    }
    plot_records(health_records, fig_labels_activities)


def plot_records(health_records: OrderedDict[date, dict], keys: Dict[str, str]):
    fig, axs = plt.subplots(len(keys))
    fig.suptitle('Health Records')

    for key, label in keys.items():
        records = []
        dates = []
        for record_date, record in health_records.items():
            dates.append(record_date)
            records.append(record[key])

        axs[list(keys.values()).index(label)].plot(dates, records)
        axs[list(keys.values()).index(label)].set(ylabel=label)

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
