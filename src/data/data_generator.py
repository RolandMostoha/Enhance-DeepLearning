import numpy as np


class DataGenerator:
    def __init__(self):
        self.input = np.ones((500, 784))
        self.y = np.ones((500, 10))
