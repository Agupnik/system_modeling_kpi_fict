from process import *
from create import *
import warnings
import pandas as pd

warnings.simplefilter(action='ignore', category=FutureWarning)

column_names = ['Average queue', 'Average load', 'Average task rate']


class Model:
    general_mean_load = 0
    general_mean_queue = 0
    Result_table = pd.DataFrame(columns=column_names)

    def __init__(self, elements_list):
        self.element_list = elements_list
        self.t_next = 0
        self.event = 0
        self.t_curr = 0
        self.stable = []
        self.mean_length_of_queue_list = list()
        self.mean_load_list = list()
        self.rate_of_completed_tasks_list = list()
        self.directive_fail_list = list()
        self.general_mean_load, self.general_mean_queue = 0.0, 0.0

    def simulate(self, time, flag):
        while self.t_curr < time:
            self.t_next = np.inf
            for element in self.element_list:
                t_next_val = np.min(element.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = element.id_element

            if flag is True:
                print("*************************************")
                print(f"Event name: {self.element_list[self.event].name}, time = {self.t_next}")
                print("*************************************")

            for element in self.element_list:
                element.statistics(self.t_next - self.t_curr)

            self.t_curr = self.t_next
            for element in self.element_list:
                element.t_curr = self.t_curr

            if len(self.element_list) > self.event:
                self.element_list[self.event].out_act()

            for element in self.element_list:
                if self.t_curr in element.t_next:
                    element.out_act()

            if len(self.element_list) > self.event and self.element_list[self.event].id_element == 0:
                self.element_list[self.event].print_event_info(flag)
            self.print_info(flag)

        self.print_result(flag)
        self.experiments()

    def print_info(self, flag):
        if flag is True:
            for element in self.element_list:
                element.print_info()

    def print_result(self, flag):
        income_task = 0
        if flag is True:
            print("\n*****************_RESULTS_*****************")
            for element in self.element_list:
                element.result()
                if isinstance(element, Create):
                    income_task = element.quantity
                elif isinstance(element, Process):
                    e = element
                    self.general_mean_load += e.mean_load / self.t_curr
                    self.general_mean_queue += e.mean_queue / self.t_curr
                    print(f"Mean length of queue: {e.mean_queue / self.t_curr}")
                    self.mean_length_of_queue_list.append(e.mean_queue / self.t_curr)
                    print(f"Max queue: {e.count_max_queue}")
                    print(f"Mean load: {e.mean_load / self.t_next}")
                    self.mean_load_list.append(e.mean_load / self.t_next)
                    print(f"Tasks that failed directive term: {e.directive_fail}")
                    self.directive_fail_list.append(e.directive_fail)
                    print(f"Rate of completed tasks: {e.quantity / income_task}")
                    self.rate_of_completed_tasks_list.append(e.quantity / income_task)
                    print()
            print()

    def experiments(self):
        avg_mean_load, avg_mean_queue = 0.0, 0.0
        income, done = 0, 0
        for e in self.element_list:
            if isinstance(e, Create):
                income = e.quantity
            elif isinstance(e, Process):
                avg_mean_load += e.mean_load / self.t_curr
                avg_mean_queue += e.mean_queue / self.t_curr
                if e.id_element == 3:
                    done = e.quantity
        Model.general_mean_load = avg_mean_load / 3
        Model.general_mean_queue = avg_mean_queue / 3
        Model.rate_task = done / income
        result = pd.DataFrame([[Model.general_mean_queue, Model.general_mean_load, Model.rate_task]],
                              columns=column_names)
        Model.Result_table = Model.Result_table.append(result, ignore_index=True)
