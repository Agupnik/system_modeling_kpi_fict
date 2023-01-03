from element import *
import numpy as np


class Process(Element):
    def __init__(self, name, distribution, channels=1, task_priority=None):
        super().__init__(name_element=name, distribution=distribution, delay=None)
        self.queue = []
        self.general_time_queue = []
        self.directive_term_queue = []
        self.left_time_queue = []
        self.queue_count = 0
        self.max_queue = np.inf
        self.mean_queue, self.mean_load = 0.0, 0.0
        self.failure = 0
        self.directive_fail = 0
        self.channel = channels
        self.t_next = [np.inf] * self.channel
        self.state = [0] * self.channel
        self.current_task = []
        self.probability = [1]
        self.task_priority = task_priority
        self.count_max_queue = 0

    def in_act(self, task_properties):
        free_route = self.get_free_channels()
        if len(free_route) > 0:
            for i in free_route:
                self.state[i] = 1
                self.current_task = task_properties
                self.delay_mean = self.current_task[self.id_element-1]
                self.t_next[i] = self.t_curr + self.delay_mean
                break
        else:
            if len(self.queue) < self.max_queue:
                self.queue.append(task_properties)
                self.general_time_queue.append(task_properties[4])
                self.directive_term_queue.append(task_properties[5])
                left_time = 0.0
                for i in range(self.id_element-1, 3):
                    left_time += task_properties[i]
                self.left_time_queue.append(left_time)
                self.queue_count += 1
            else:
                self.failure += 1

    def out_act(self):
        current_channel = self.get_current_channel()
        for i in current_channel:
            super().out_act()
            self.t_next[i] = np.inf
            self.state[i] = 0
            if self.next_element is not None:
                next_el = np.random.choice(a=self.next_element, p=self.probability)
                next_el.in_act(self.current_task)
            else:
                if self.t_curr > self.current_task[5]:
                    self.directive_fail += 1
            self.current_task = []

            if len(self.queue) > 0:
                if self.task_priority == "lowest general time":
                    task_index = self.general_time_queue.index(min(self.general_time_queue))
                elif self.task_priority == "highest general time":
                    task_index = self.general_time_queue.index(max(self.general_time_queue))
                elif self.task_priority == "lowest time of left processing":
                    task_index = self.left_time_queue.index(min(self.left_time_queue))
                elif self.task_priority == "closest directive term":
                    task_index = self.directive_term_queue.index(min(self.directive_term_queue))
                else:
                    task_index = -1
                self.queue_count -= 1
                self.state[i] = 1
                self.current_task = self.queue.pop(task_index)
                self.general_time_queue.pop(task_index)
                self.directive_term_queue.pop(task_index)
                self.left_time_queue.pop(task_index)
                self.delay_mean = self.current_task[self.id_element - 1]
                self.t_next[i] = self.t_curr + self.delay_mean

    def get_free_channels(self):
        free_channels = []
        for i in range(self.channel):
            if self.state[i] == 0:
                free_channels.append(i)
        return free_channels

    def get_current_channel(self):
        current_channels = []
        for i in range(self.channel):
            if self.t_next[i] == self.t_curr:
                current_channels.append(i)
        return current_channels

    def print_info(self):
        super().print_info()
        print(f"Current count of awaiting tasks: {self.queue_count}")
        print(f"General time processing queue: {self.general_time_queue}")
        print(f"Directive terms queue: {self.directive_term_queue}")
        print(f"Task ending processing time queue: {self.left_time_queue}")
        print()

    def statistics(self, delta):
        self.mean_queue += len(self.queue) * delta
        if self.queue_count > self.count_max_queue:
            self.count_max_queue = self.queue_count
        for i in range(self.channel):
            self.mean_load += self.state[i] * delta
