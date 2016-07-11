from math import sin
from math import pi
import numpy as np

__author__ = 'sean_moorhead'

def lc_fit_function(time, freq, ampl, phase):
    val = (ampl * sin(2 * pi * (freq * time + phase)))
    return val
