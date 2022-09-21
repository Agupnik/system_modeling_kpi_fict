import fun_rand as fun


class Element:
    nextId = 0

    def __init__(self, delay=None, distribution=None):
        self.t_next = [0]  # момент часу наступної події
        self.delay_mean = delay  # середнє значення часової затримки
        self.delay_dev = None  # середнє квадратичне відхилення часової затримки
        self.quantity = 0
        self.t_curr = self.t_next  # поточний момент часу
        self.state = [0]
        self.next_element = None  # вказує на наступний (в маршруті слідування вимоги) елемент моделі
        self.id_el = Element.nextId
        Element.nextId += 1
        self.name = 'Element' + str(self.id_el)
        self.distribution = distribution
        self.probability = [1]

    def get_delay(self):
        if 'exp' == self.distribution:
            return fun.exp(self.delay_mean)
        elif 'norm' == self.distribution:
            return fun.norm(self.delay_mean, self.delay_dev)
        elif 'uniform' == self.distribution:
            return fun.uniform(self.delay_mean, self.delay_dev)
        else:
            return self.delay_mean

    def in_act(self):  # вхід в елемент
        pass

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def set_t_next(self, t_next_new):
        self.t_next = t_next_new

    def get_t_curr(self):
        return self.t_curr

    def out_act(self):  # вихід з елементу
        self.quantity += 1

    def result(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def print_info(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} t_next = {self.t_next}')

    def calculate(self, delta):
        pass

    def calculate_mean(self, delta):
        pass
