from element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def out_act(self):
        super().out_act()
        self.t_next[0] = self.t_curr + super().get_delay()

        next_element = self.choose_next_element()
        next_element.in_act()
