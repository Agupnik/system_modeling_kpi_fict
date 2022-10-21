from create import Create
from model import Model
from process import Process
import random


def build_simple_model(n: int):
    c1 = Create(delay_mean=random.randint(1, 5), name='CREATOR', distribution='exp')
    p_prev = c1
    elements = [c1]
    for i in range(n - 1):
        p = Process(delay_mean=random.randint(1, 5), distribution='exp')
        p_prev.next_element = [p]
        elements.append(p)
        p_prev = p
    p = Process(n_channel=2, delay_mean=random.randint(1, 5), distribution='exp')
    p_prev.next_element = [p]
    elements.append(p)
    model = Model(elements)
    return c1, model


def build_complex_model(n: int):
    c1 = Create(delay_mean=random.randint(1, 5), name='CREATOR', distribution='exp')
    p_prev = c1
    elements = [c1]
    for i in range(int(n / 5)):
        p = Process(delay_mean=random.randint(1, 5), distribution='exp')
        p_prev.next_element = [p]
        p1 = Process(delay_mean=random.randint(1, 5), distribution='exp')
        p2 = Process(delay_mean=random.randint(1, 5), distribution='exp')
        p.next_element = [p1, p2]
        p.probability = [0.7, 0.3]
        if i != int(n / 5) - 1:
            p3 = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p1.next_element = [p3]
            p2.next_element = [p3]
            p4 = Process(delay_mean=random.randint(1, 5), distribution='exp')
            p3.next_element = [p4]
            p_prev = p4
            elements.append(p)
            elements.append(p1)
            elements.append(p2)
            elements.append(p3)
            elements.append(p4)
        else:
            p3 = Process(n_channel=2, delay_mean=random.randint(1, 5), distribution='exp')
            p1.next_element = [p3]
            p2.next_element = [p3]
            elements.append(p)
            elements.append(p1)
            elements.append(p2)
            elements.append(p3)
            p3.channel = 2
    model = Model(elements)
    return c1, model
