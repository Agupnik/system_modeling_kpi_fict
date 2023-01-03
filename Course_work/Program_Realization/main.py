from model import *
from process import *
import matplotlib.pyplot as plt


def sim_response(modeling_time, test_times, queue_type):
    times = 0
    while times < test_times:
        start_model(False, modeling_time, queue_type, None)
        times += 1


def sim_verify(modeling_time, test_times):
    n_params = 11

    order_income_min_value = [100, 0, 100, 100, 100, 100, 100, 100, 100, 100, 100]
    order_income_max_value = [200, 200, 1000, 200, 200, 200, 200, 200, 200, 200, 200]
    programming = [120, 120, 120, 0, 500, 120, 120, 120, 120, 120, 120]
    write = [110, 110, 110, 110, 110, 0, 500, 110, 110, 110, 110]
    testing = [90, 90, 90, 90, 90, 90, 90, 0, 500, 90, 90]
    additional_tech_time_min_value = [20, 20, 20, 20, 20, 20, 20, 20, 20, 0, 20]
    additional_tech_time_max_value = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 1000]

    queue_types = ['lowest general time',
                   'highest general time',
                   'lowest time of left processing',
                   'closest directive term']

    for queue_type in queue_types:
        df = pd.DataFrame()
        rows = []
        for i in range(n_params):
            times = 0
            mean_length_of_queue_programming = list()
            mean_length_of_queue_write = list()
            mean_length_of_queue_testing = list()

            mean_load_programming = list()
            mean_load_write = list()
            mean_load_testing = list()

            rate_of_completed_tasks_programming = list()
            rate_of_completed_tasks_write = list()
            rate_of_completed_tasks_testing = list()

            directive_fail_programming = list()
            directive_fail_write = list()
            directive_fail_testing = list()

            while times < test_times:
                create = Create('INCOMING TASK',
                                'uniform',
                                [order_income_min_value[i], order_income_max_value[i]],
                                programming[i],
                                write[i],
                                testing[i],
                                [additional_tech_time_min_value[i], additional_tech_time_max_value[i]])
                model = start_model(False, modeling_time, queue_type, create)
                model.print_result(True)

                mean_length_of_queue_programming.append(model.mean_length_of_queue_list[0])
                mean_length_of_queue_write.append(model.mean_length_of_queue_list[1])
                mean_length_of_queue_testing.append(model.mean_length_of_queue_list[2])

                mean_load_programming.append(model.mean_load_list[0])
                mean_load_write.append(model.mean_load_list[1])
                mean_load_testing.append(model.mean_load_list[2])

                rate_of_completed_tasks_programming.append(model.rate_of_completed_tasks_list[0])
                rate_of_completed_tasks_write.append(model.rate_of_completed_tasks_list[1])
                rate_of_completed_tasks_testing.append(model.rate_of_completed_tasks_list[2])

                directive_fail_programming.append(model.directive_fail_list[0])
                directive_fail_write.append(model.directive_fail_list[1])
                directive_fail_testing.append(model.directive_fail_list[2])

                times += 1

            param = {'order_income_min_value': order_income_min_value[i],
                     'order_income_max_value': order_income_max_value[i],
                     'programming': programming[i],
                     'write': write[i],
                     'testing': testing[i],
                     'additional_tech_time_min_value': additional_tech_time_min_value[i],
                     'additional_tech_time_max_value': additional_tech_time_max_value[i],
                     'mean_length_of_queue_programming': sum(mean_length_of_queue_programming) / len(mean_length_of_queue_programming),
                     'mean_length_of_queue_write': sum(mean_length_of_queue_write) / len(mean_length_of_queue_write),
                     'mean_length_of_queue_testing': sum(mean_length_of_queue_testing) / len(mean_length_of_queue_testing),
                     'mean_load_programming': sum(mean_load_programming) / len(mean_load_programming),
                     'mean_load_writ': sum(mean_load_write) / len(mean_load_write),
                     'mean_load_testing': sum(mean_load_testing) / len(mean_load_testing),
                     'rate_of_completed_tasks_programming': sum(rate_of_completed_tasks_programming) / len(rate_of_completed_tasks_programming),
                     'rate_of_completed_tasks_write': sum(rate_of_completed_tasks_write) / len(rate_of_completed_tasks_write),
                     'rate_of_completed_tasks_testing': sum(rate_of_completed_tasks_testing) / len(rate_of_completed_tasks_testing),
                     'directive_fail_programming': sum(directive_fail_programming) / len(directive_fail_programming),
                     'directive_fail_write': sum(directive_fail_write) / len(directive_fail_write),
                     'directive_fail_testing': sum(directive_fail_testing) / len(directive_fail_testing)}

            rows.append({**param})

        file_name = f'{queue_type}_verification.xlsx'

        df = df.append(rows)
        df.to_excel(file_name)

    print("Результати верификації записані у відповідні файли!!!")


def sim(flag, modeling_time, test_times, task_priority):
    times = 0
    while times < test_times:
        start_model(flag, modeling_time, task_priority, None)
        times += 1
    print(Model.Result_table)


def start_model(flag, modeling_time, task_priority, create_val):
    # lowest general time
    # highest general time
    # lowest time of left processing
    # closest directive term

    if create_val is not None:
        create = create_val
    else:
        Element.next_id = 0
        create = Create('INCOMING TASK', 'uniform', [100.0, 200.0], 120.0, 110.0, 90.0, [20.0, 60.0])

    process_1 = Process(name='PROGRAMMING', distribution='exp', task_priority=task_priority)
    process_2 = Process(name='WRITE ON CARRIER', distribution='exp', task_priority=task_priority)
    process_3 = Process(name='TESTING', distribution='exp', task_priority=task_priority)

    create.next_element = [process_1]
    process_1.next_element = [process_2]
    process_2.next_element = [process_3]

    elements_list = [create, process_1, process_2, process_3]
    model = Model(elements_list)
    model.simulate(modeling_time, flag)

    Element.next_id = 0

    return model


def select_queuing_type(flag, test_times, modeling_time):
    print("Оберіть тип черговості обробки замовлень")
    print("1 - Найменше загального часу обробки.")
    print("2 - Найбільше загального часу обробки.")
    print("3 - Найменший час обробки, що залишився.")
    print("4 - Найближчий директивний термін.")
    task = input()
    if task == "1":
        sim(flag, modeling_time, test_times, "lowest general time")
        Model.Result_table.to_excel(r'lowest_general_time.xlsx', sheet_name='1', index=False)
    elif task == "2":
        sim(flag, modeling_time, test_times, "highest general time")
        Model.Result_table.to_excel(r'highest_general_time.xlsx', sheet_name='1', index=False)
    elif task == "3":
        sim(flag, modeling_time, test_times, "lowest time of left processing")
        Model.Result_table.to_excel(r'lowest_time_of_left_processing.xlsx', sheet_name='1', index=False)
    elif task == "4":
        sim(flag, modeling_time, test_times, "closest directive term")
        Model.Result_table.to_excel(r'closest_directive_term.xlsx', sheet_name='1', index=False)
    else:
        print("Ви повинні вибрати відповідне завдання!")
        main()


def main():
    print("Привіт! Чи повинні ми реєструвати повну інформацію про моделювання? (Введіть номер і натисніть enter)")
    print("1 - Так.")
    print("2 - Ні.")
    print("3 - Мені потрібен відгук алгоритму при збільшенні часу моделювання.")
    print("4 - Мені потрібно провести верифікацію моделі.")
    task = input()
    # 100000
    modeling_time = 100000
    test_times = 2000
    if task == "1":
        select_queuing_type(True, test_times, modeling_time)
    elif task == "2":
        select_queuing_type(False, test_times, modeling_time)
    elif task == "3":
        queue_types = ['lowest general time',
                       'highest general time',
                       'lowest time of left processing',
                       'closest directive term']

        for queue_type in queue_types:
            start_time = 500
            response_list1 = list()
            response_list2 = list()
            time_list = list()
            test = 1
            while test < 101:
                sim_response(start_time, test_times, queue_type)
                response_list1.append(Model.Result_table['Average load'].mean())
                response_list2.append(Model.Result_table['Average queue'].mean())
                time_list.append(start_time)
                Model.Result_table = pd.DataFrame(columns=column_names)
                test += 1
                start_time += 500
            plt.plot(time_list, response_list1)
            plt.xlabel(f'Час моделювання (од.) ({queue_type})')
            plt.ylabel('Середня завантаженість системи')
            plt.title('Відношення часу моделювання до значення відгуку')
            plt.show()
            plt.plot(time_list, response_list2, 'g')
            plt.xlabel(f'Час моделювання (од.) ({queue_type})')
            plt.ylabel('Середнє значення черг')
            plt.title('Відношення часу моделювання до значення відгуку')
            plt.show()
            print(queue_type)
            print(response_list1)
            print(response_list2)
            print(time_list)
            print(len(time_list))
    elif task == "4":
        sim_verify(modeling_time, test_times)
    else:
        print("Ви повинні вибрати відповідне завдання!")
        main()


if __name__ == "__main__":
    main()
