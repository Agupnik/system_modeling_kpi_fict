import random
import numpy as np
from gen import Generator


class Generator3(Generator):
    def __init__(self, num_of_values, a, c):
        self.a = a
        self.c = c
        super().__init__(num_of_values, self.calculate_uniform)

    def create_array(self):
        z = self.a * random.random() % self.c

        x_array = np.array([])
        for i in range(0, self.num_of_values):
            z = self.a * z % self.c
            x_array = np.append(x_array, z / self.c)

        return x_array

    def calculate_uniform(self, interval_list, i):
        return (interval_list[i][1] - interval_list[i][0]) / (max(self.array) - min(self.array))
