import numpy as np
import util


class Generator:
    def __init__(self, num_of_values, function):
        self.num_of_values = num_of_values
        self.array = self.create_array()
        self.function = function

    def create_array(self):
        return np.array([])

    def get_expected_values(self, entries, num_of_intervals):
        expected_list = list()
        interval_list = util.pull_intervals_from_list(entries, num_of_intervals)

        for i in range(num_of_intervals):
            expected_list.append(self.function(interval_list, i))

        return expected_list

    def analyze(self, num_of_intervals):
        average, dispersion = util.get_average_and_dispersion(self.array)

        entries = util.get_intervals(self.array, num_of_intervals)
        util.plot_histogram(entries, num_of_intervals)

        expected_list = self.get_expected_values(entries, num_of_intervals)
        observed_list = [i[1] for i in entries]

        observed_chi_squared, expected_chi_squared = util.chi_2_tool(expected_list, observed_list, num_of_intervals)

        util.print_extra_info(average, dispersion, observed_chi_squared, expected_chi_squared,
                              observed_chi_squared < expected_chi_squared)
