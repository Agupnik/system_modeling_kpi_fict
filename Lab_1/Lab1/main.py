from gen1 import Generator1
from gen2 import Generator2
from gen3 import Generator3

num_of_values = 10000
bins = 20
num_of_test = 3
list_of_lambda = [0.5, 0.3, 15]

for lambda_val in list_of_lambda:
    print(f'\t###__Lambda = {lambda_val}__###')
    generator_1 = Generator1(lambda_val, num_of_values)
    generator_1.analyze(bins)
    print()

list_of_alpha = [2, 10, 5]
list_of_sigma = [1, 5, 7]

for i in range(0, num_of_test):
    print(f'\t###__Alpha = {list_of_alpha[i]}; Sigma = {list_of_sigma[i]}__###')
    generator_2 = Generator2(list_of_alpha[i], list_of_sigma[i], num_of_values)
    generator_2.analyze(bins)
    print()

list_of_a = [pow(5, 13), pow(5, 6), pow(5, 12)]
list_of_c = [pow(2, 31), pow(2, 15), pow(2, 10)]


for i in range(0, num_of_test):
    print(f'\t###__A = {list_of_a[i]}; C = {list_of_c[i]}__###')
    generator_3 = Generator3(num_of_values, list_of_a[i], list_of_c[i])
    generator_3.analyze(bins)
    print()
