from create import Create
from tabulate import tabulate
from model import Model
from process import Process
import pandas as pd


# c = Create(5)
#
# p1 = Process(5)
#
# p1.max_queue = 5
#
# c.distribution = 'exp'
# p1.distribution = 'exp'
#
# c.name = 'Creator'
# p1.name = 'Process 1'
#
# c.next_element = p1
# p1.is_next_dispose = True
#
# elements = [c, p1]
# model = Model(elements)
# res = model.simulate(1000)


n_param = 20

delay_create_list =   [4, 10, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 0.5, 4, 4, 4, 4, 4, 4]
delay_process1_list = [4, 4, 10, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 0.5, 4, 4, 4, 4, 4]
delay_process2_list = [4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 0.5, 4, 4, 4, 4]
delay_process3_list = [4, 4, 4, 4, 10, 4, 4, 4, 4, 4, 4, 4, 1, 4, 4, 4, 0.5, 4, 4, 4]
maxQ_list1 =          [5, 5, 5, 5, 5, 10, 5, 5, 1, 1, 1, 1, 1, 5, 5, 5, 5, 1, 5, 5]
maxQ_list2 =          [5, 5, 5, 5, 5, 5, 10, 5, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 1, 5]
maxQ_list3 =          [5, 5, 5, 5, 5, 5, 5, 10, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 1]
distribution = ['exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp',
                'exp', 'exp', 'exp', 'exp', 'exp', 'exp', 'exp']

df = pd.DataFrame()
rows = []

for i in range(n_param):
    c = Create(delay_create_list[i])

    p1 = Process(delay_process1_list[i])
    p2 = Process(delay_process2_list[i])
    p3 = Process(delay_process3_list[i])

    p1.max_queue = maxQ_list1[i]
    p2.max_queue = maxQ_list2[i]
    p3.max_queue = maxQ_list3[i]

    c.distribution = distribution[i]
    p1.distribution = distribution[i]
    p2.distribution = distribution[i]
    p3.distribution = distribution[i]

    c.name = 'Creator'
    p1.name = 'Process 1'
    p2.name = 'Process 2'
    p3.name = 'Process 3'

    c.next_element = p1
    p1.next_processes.append(p2)
    p2.next_processes.append(p3)
    p3.is_next_dispose = True

    elements = [c, p1, p2, p3]
    model = Model(elements)
    res = model.simulate(1000)

    param = {'delay_create': delay_create_list[i],
             'delay_process1': delay_process1_list[i],
             'delay_process2': delay_process2_list[i],
             'delay_process3': delay_process3_list[i],
             'max_queue1': maxQ_list1[i],
             'max_queue2': maxQ_list2[i],
             'max_queue3': maxQ_list3[i],
             'process1_processed': p1.quantity,
             'process1_failed': p1.failure,
             'process2_processed': p2.quantity,
             'process2_failed': p2.failure,
             'process3_processed': p3.quantity,
             'process3_failed': p3.failure,
             'distribution': distribution[i]}

    rows.append({**param, **res})

# назва файлу xlsx
file_name = 'ModelData.xlsx'

# імпорт в Excel
df = df.append(rows)
df.to_excel(file_name)
print(tabulate(df, headers='keys', tablefmt='fancy_grid', numalign="center"))
