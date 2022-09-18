import random as rnd
import element as e


class Process(e.Element):
    def __init__(self, delay):
        super().__init__(delay)
        self.queue = 0
        self.max_observed_queue = 0
        self.max_queue = float('inf')
        self.mean_queue = 0.0
        self.failure = 0
        self.next_processes = []
        self.mean_load = 0
        self.delta_tr = 0
        self.max_delta_tr = 0
        self.is_next_dispose = False

    def in_act(self):
        if super().get_state() == 0:
            super().set_state(1)
            super().set_t_next(super().get_t_curr() + super().get_delay())
        else:
            if self.queue < self.max_queue:
                self.queue += 1
            else:
                self.failure += 1

    def out_act(self):
        super().out_act()
        self.set_t_next(float('inf'))
        self.set_state(0)

        if self.queue > 0:
            self.queue -= 1
            self.set_state(1)
            self.t_next = self.t_curr + self.get_delay()

        if len(self.next_processes) > 0:
            if not self.is_next_dispose:
                index = rnd.randint(0, len(self.next_processes) - 1)
            else:
                index = rnd.randint(0, len(self.next_processes))
            if index != len(self.next_processes):
                self.next_processes[index].in_act()

    def print_info(self):
        super().print_info()
        print(f'failure = {str(self.failure)}, queue_length = {str(self.queue)}')

    def calculate(self, delta):
        self.mean_queue += self.queue * delta

        if self.queue > self.max_observed_queue:
            self.max_observed_queue = self.queue

        self.delta_tr += delta * self.state

        if delta*self.state > self.max_delta_tr:
            self.max_delta_tr = delta * float(self.state)
