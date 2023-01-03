from fun_rand import *


class Element:
    next_id = 0

    def __init__(self, name_element=None, delay=None, distribution=None):
        self.next_element = None
        self.t_next = [0]
        self.t_curr = self.t_next
        self.state = [0]
        self.id_element = Element.next_id
        Element.next_id += 1
        self.name = name_element
        self.quantity = int()
        self.delay_dev = float()
        self.delay_mean = float()
        self.distribution = str()
        self.probability = [1]
        self.delay_mean = delay
        self.distribution = distribution

    def get_delay(self):
        if self.distribution == 'exp':
            delay = exp(self.delay_mean)
        elif self.distribution == 'uniform':
            delay = uniform(self.delay_mean, self.delay_dev)
        else:
            delay = self.delay_mean
        return delay

    def in_act(self, priority):
        pass

    def out_act(self):
        self.quantity += 1

    def statistics(self, delta):
        pass

    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def print_info(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} t_next = {self.t_next}')
