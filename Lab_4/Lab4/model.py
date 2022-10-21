import numpy as np

from element import Element


class Model:
    def __init__(self, elements: list[Element]):
        self.list = elements
        self.event = 0
        self.t_next = 0.0
        self.t_curr = self.t_next

    def simulate(self, time):
        while self.t_curr < time:
            self.t_next = float('inf')

            for e in self.list:
                t_next_val = np.min(e.t_next)
                if t_next_val < self.t_next:
                    self.t_next = t_next_val
                    self.event = e.id_el

            self.t_curr = self.t_next

            for e in self.list:
                e.t_curr = self.t_curr

            if len(self.list) > self.event:
                self.list[self.event].out_act()

            for e in self.list:
                if self.t_curr in e.t_next:
                    e.out_act()
