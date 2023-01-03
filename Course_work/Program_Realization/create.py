from element import *


class Create(Element):
    def __init__(self, name, distribution, interval1, elem1_delay, elem2_delay, elem3_delay, interval2):
        super().__init__(name_element=name, distribution=distribution, delay=interval1[0])
        self.delay_dev = interval1[1]
        self.delay1 = elem1_delay
        self.delay2 = elem2_delay
        self.delay3 = elem3_delay
        self.elem1_delay = 0.0
        self.elem2_delay = 0.0
        self.elem3_delay = 0.0
        self.add_time_min = interval2[0]
        self.add_time_max = interval2[1]
        self.general_time = 0.0
        self.technical_time = 0.0
        self.add_time = 0.0
        self.properties = []

    def out_act(self):
        super().out_act()
        self.elem1_delay = exp(self.delay1)
        self.elem2_delay = exp(self.delay2)
        self.elem3_delay = exp(self.delay3)
        self.add_time = uniform(self.add_time_min, self.add_time_max)
        self.general_time = self.elem1_delay + self.elem2_delay + self.elem3_delay
        self.technical_time = self.general_time + self.add_time
        delay = uniform(self.delay_mean, self.delay_dev)
        self.t_next[0] = self.t_curr + delay
        directive_term = self.t_curr + self.technical_time + delay
        self.properties = [
            self.elem1_delay,
            self.elem2_delay,
            self.elem3_delay,
            self.add_time,
            self.general_time,
            directive_term]
        self.next_element[0].in_act(self.properties)

    def print_event_info(self, flag):
        if flag is True:
            print(f"Programming delay: {self.properties[0]}")
            print(f"Write on carrier delay: {self.properties[1]}")
            print(f"Testing delay: {self.properties[2]}")
            print(f"Technical delay: {self.technical_time}")
            print(f"Directive term: {self.properties[5]}")
            print()
