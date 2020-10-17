import abc
from datetime import date
from typing import Dict

from data.model.records import HeartRecord, BodyRecord


class DataProvider(abc.ABC):

    @abc.abstractmethod
    def get_heart_records(self) -> Dict[date, HeartRecord]:
        pass

    @abc.abstractmethod
    def get_body_records(self) -> Dict[date, BodyRecord]:
        pass
