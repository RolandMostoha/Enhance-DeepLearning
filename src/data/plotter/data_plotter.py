from datetime import date
from typing import OrderedDict

import matplotlib.pyplot as plt

from data.model.records import RECORD_KEYS


def plot(health_records: OrderedDict[date, dict]):
    fig, axs = plt.subplots(len(RECORD_KEYS))
    fig.suptitle('Health Records')

    for key in RECORD_KEYS:
        records = []
        dates = []
        for record_date, record in health_records.items():
            dates.append(record_date)
            records.append(record[key])

        axs[RECORD_KEYS.index(key)].plot(dates, records)
        axs[RECORD_KEYS.index(key)].set(ylabel=key)

    fig.autofmt_xdate()
    plt.show()
