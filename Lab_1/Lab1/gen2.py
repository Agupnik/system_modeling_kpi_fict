import random
import numpy as np
import util
from numpy import random
from gen import Generator


def get_myu():
    myu = 0
    for i in range(0, 12):
        myu += random.random()
    return myu - 6


class Generator2(Generator):
    def __init__(self, alpha, sigma, num_of_values):
        self.alpha = alpha
        self.sigma = sigma
        super().__init__(num_of_values, self.calculate_normal)

    def create_array(self):
        x_array = np.array([])
        for i in range(0, self.num_of_values):
            myu = get_myu()
            x_array = np.append(x_array, self.sigma * myu + self.alpha)
        return x_array

    def calculate_normal(self, interval_list, i):
        num = util.normal_fun(interval_list[i][0], interval_list[i][1], self.alpha, self.sigma)
        return num
