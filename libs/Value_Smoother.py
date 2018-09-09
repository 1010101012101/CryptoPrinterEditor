import math

def linear_changer(value):
    return (-abs(value) + 100)

def exponential_changer(value):
    return math.pow(1.1, - abs(value) + 48.3)

def exponential_smoother(value):
    return math.pow(value*1000,1/3)