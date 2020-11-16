from pandas import DataFrame
from sklearn.model_selection import train_test_split


class DatasetGenerator:

    def __init__(self, data_frame: DataFrame, target_feature: str):
        self.y = data_frame[target_feature]
        self.x = data_frame.drop(columns=[target_feature])

        self.x_train = None
        self.y_train = None
        self.x_valid = None
        self.y_valid = None
        self.x_test = None
        self.y_test = None

    def split(self, train_ratio: float, valid_ratio: float, test_ratio: float):
        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y, test_size=1 - train_ratio)
        val_ratio = test_ratio / (test_ratio + valid_ratio)
        x_valid, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=val_ratio)

        self.x_train = x_train
        self.y_train = y_train
        self.x_valid = x_valid
        self.y_valid = y_val
        self.x_test = x_test
        self.y_test = y_test
