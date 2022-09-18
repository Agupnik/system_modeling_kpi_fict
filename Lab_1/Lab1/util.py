import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import integrate

# k - The number of degrees of freedom
# Level of significance a = 0.05
hi_squared_table = {
    1: 3.8,
    2: 6.0,
    3: 7.8,
    4: 9.5,
    5: 11.1,
    6: 12.6,
    7: 14.1,
    8: 15.5,
    9: 16.9,
    10: 18.3,
    11: 19.7,
    12: 21.0,
    13: 22.4,
    14: 23.7,
    15: 25.0,
    16: 26.3,
    17: 27.6,
    18: 28.9,
    19: 30.1,
    20: 31.4,
    21: 32.7,
    22: 33.9,
    23: 35.2,
    24: 36.4,
    25: 37.7,
    26: 38.9,
    27: 40.1,
    28: 41.3,
    29: 42.6,
    30: 43.8
}


def find_table_hi_squared(x):
    return hi_squared_table[x]


def print_name(num):
    print('\t###__GENERATOR #' + str(num) + '__###')


def print_extra_info(average, dispersion, observed_chi_2, expected_chi_2, result):
    print('\nChi squared (observed): ' + str(observed_chi_2))
    print('Chi squared (expected): ' + str(expected_chi_2))
    print('The found distribution law corresponds to the observed values of the random variable: ' + str(result))
    print('Average: ' + str(average))
    print('Dispersion: ' + str(dispersion))


def get_average_and_dispersion(array):
    s = 0
    average = array.sum() / array.size

    for i in array:
        s += pow(i - average, 2)

    dispersion = s / (array.size - 1)
    return average, dispersion


def get_intervals(array, num_of_intervals):
    interval_size = (array.max() - array.min()) / num_of_intervals

    entries_list = list()
    limit_1 = array.min()

    for i in range(0, num_of_intervals):
        limit_2 = limit_1 + interval_size

        counter = 0
        for n in array:
            if limit_1 <= n < limit_2:
                counter += 1

        entries_list.append([[limit_1, limit_2], counter])
        limit_1 = limit_2

    return entries_list


def pull_intervals_from_list(entries, num_of_intervals):
    interval_list = list()
    for i in range(num_of_intervals):
        interval_list.append([entries[i][0][0], entries[i][0][1]])
    return interval_list


def to_data_frame(arr, num_of_intervals):
    copy_arr = [x[:] for x in arr]
    for i in range(num_of_intervals):
        name_interval = str(round(copy_arr[i][0][0], 2)) + '-' + str(round(copy_arr[i][0][1], 2))
        copy_arr[i][0] = name_interval

    df = pd.DataFrame(copy_arr, columns=['Intervals', 'Values'])
    return df


def plot_histogram(entries_list, num_of_intervals):
    df_e = to_data_frame(entries_list, num_of_intervals)

    print(df_e.head(num_of_intervals))

    sns.barplot(data=df_e, x='Intervals', y='Values', color='g', edgecolor='black')
    plt.tight_layout()
    plt.xticks(rotation=29)
    plt.show()


def chi_2_tool(expected_list, observed_list, num_of_intervals):
    observed_chi_squared = 0
    for i in range(num_of_intervals):
        expected = 10000 * expected_list[i]
        observed_chi_squared += pow(observed_list[i] - expected, 2) / expected
    expected_chi_squared = find_table_hi_squared(num_of_intervals - 1)
    return observed_chi_squared, expected_chi_squared


def exp_fun(zero, first, lambda_num):
    v = np.exp(-lambda_num*zero) - np.exp(-lambda_num*first)
    return v


def normal_fun(zero, first, alpha, sigma):
    def f(x):
        return 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(- (x - alpha)**2 / (2 * sigma**2))
    v, err = integrate.quad(f, zero, first)
    return v

