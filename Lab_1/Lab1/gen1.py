import random
import numpy as np
import util


class Generator1:
    def __init__(self, lambda_value, num_of_values):
        self.average = None
        self.lambda_value = lambda_value
        self.num_of_values = num_of_values
        self.array = []

    def create_array(self):
        x_array = np.array([])
        for i in range(0, self.num_of_values):
            ksi = random.random()
            x_array = np.append(x_array, -np.log(ksi) / self.lambda_value)
        self.average = np.average(x_array)
        self.array = x_array
        return x_array

    def get_expected_values(self, entries, num_of_intervals):
        expected_list = list()
        interval_list = util.pull_intervals_from_list(entries, num_of_intervals)

        for i in range(num_of_intervals):
            expected_list.append(self.calculate_exponential(interval_list, i))

        return expected_list

    def calculate_exponential(self, interval_list, i):
        return util.exp_fun(interval_list[i][0], interval_list[i][1], self.lambda_value)

    def analyze(self, num_of_intervals):
        util.print_name(1)

        array = self.create_array()
        average, dispersion = util.get_average_and_dispersion(array)

        entries = util.get_intervals(array, num_of_intervals)
        util.plot_histogram(entries, num_of_intervals)

        expected_list = self.get_expected_values(entries, num_of_intervals)
        observed_list = [i[1] for i in entries]

        observed_chi_squared, expected_chi_squared = util.chi_2_tool(expected_list, observed_list, num_of_intervals)

        util.print_extra_info(average, dispersion, observed_chi_squared, expected_chi_squared,
                              observed_chi_squared < expected_chi_squared)