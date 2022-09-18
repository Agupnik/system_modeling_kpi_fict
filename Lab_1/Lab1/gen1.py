import random
import numpy as np
import util
from gen import Generator


class Generator1(Generator):
    def __init__(self, lambda_value, num_of_values):
        self.lambda_value = lambda_value
        super().__init__(num_of_values, self.calculate_exponential)

    def create_array(self):
        x_array = np.array([])
        for i in range(0, self.num_of_values):
            ksi = random.random()
            x_array = np.append(x_array, -np.log(ksi) / self.lambda_value)
        return x_array

    def calculate_exponential(self, interval_list, i):
        return util.exp_fun(interval_list[i][0], interval_list[i][1], self.lambda_value)
