import random
import numpy as np
import util


def calculate(array, interval_list, i):
    return (interval_list[i][1] - interval_list[i][0]) / (max(array) - min(array))


def get_expected_values(array, entries, num_of_intervals):
    expected_list = list()
    interval_list = util.pull_intervals_from_list(entries, num_of_intervals)

    for i in range(num_of_intervals):
        expected_list.append(calculate(array, interval_list, i))
    return expected_list


class Generator3:
    def __init__(self, num_of_values, a, c):
        self.a = a
        self.c = c
        self.num_of_values = num_of_values

    def create_array(self):
        z = self.a * random.random() % self.c

        x_array = np.array([])
        for i in range(0, self.num_of_values):
            z = self.a * z % self.c
            x_array = np.append(x_array, z / self.c)

        return x_array

    def analyze(self, num_of_intervals):
        util.print_name(3)

        array = self.create_array()
        average, dispersion = util.get_average_and_dispersion(array)

        entries = util.get_intervals(array, num_of_intervals)
        util.plot_histogram(entries, num_of_intervals)

        expected_list = get_expected_values(array, entries, num_of_intervals)
        observed_list = [i[1] for i in entries]

        observed_chi_squared, expected_chi_squared = util.chi_2_tool(expected_list, observed_list, num_of_intervals)

        util.print_extra_info(average, dispersion, observed_chi_squared, expected_chi_squared,
                              observed_chi_squared < expected_chi_squared)
