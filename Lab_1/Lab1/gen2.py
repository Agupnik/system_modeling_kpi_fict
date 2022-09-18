import random
import numpy as np
import util
from numpy import random


def get_myu():
    myu = 0
    for i in range(0, 12):
        myu += random.random()
    return myu - 6


class Generator2:
    def __init__(self, alpha, sigma, num_of_values):
        self.alpha = alpha
        self.sigma = sigma
        self.num_of_values = num_of_values

    def create_array(self):
        x_array = np.array([])
        for i in range(0, self.num_of_values):
            myu = get_myu()
            x_array = np.append(x_array, self.sigma * myu + self.alpha)
        return x_array

    def get_expected_values(self, entries, num_of_intervals):
        expected_list = list()
        interval_list = util.pull_intervals_from_list(entries, num_of_intervals)

        for i in range(num_of_intervals):
            expected_list.append(self.calculate_normal(interval_list, i))
        return expected_list

    def calculate_normal(self, interval_list, i):
        num = util.normal_fun(interval_list[i][0], interval_list[i][1], self.alpha, self.sigma)
        return num

    def analyze(self, num_of_intervals):
        util.print_name(2)

        array = self.create_array()
        average, dispersion = util.get_average_and_dispersion(array)

        entries = util.get_intervals(array, num_of_intervals)
        util.plot_histogram(entries, num_of_intervals)

        observed_list = [i[1] for i in entries]

        expected_list = self.get_expected_values(entries, num_of_intervals)

        observed_chi_squared, expected_chi_squared = util.chi_2_tool(expected_list, observed_list, num_of_intervals)

        util.print_extra_info(average, dispersion, observed_chi_squared, expected_chi_squared,
                              observed_chi_squared < expected_chi_squared)
