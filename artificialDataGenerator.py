from __future__ import division
from DataPoint import DataPoint
from FitFunctions import lc_fit_function
from Curve import Curve


__author__ = 'sean_moorhead'

OUT_FILE = "../PG1159-035/artificialData/1993_March.dat"
SEC_IN_YEAR = 31557600  # 1 year = 365.25 days,  1 day = 24 hours
STEP = 10 # step size for data points in seconds
START_DATE = 1993.25 # in years
END_DATE = 1993.28 # in years


'''
The following three functions denote how each parameter will vary with time in the data.
Remember that the incoming time is in * seconds *
'''


def frequency_func(time):
    return (1.0 / 516.0)


# this function is currently the decay rate of the amplitude in the 516s mode
# as found from a fit to the points of the amplitude over various years
def amplitude_func(time):
    yrs = time / SEC_IN_YEAR
    a = 0.0387185301
    b = -154.223977
    c = 153582.413
    val = ((a * (yrs ** 2)) + (b * yrs) + c)
    return val


def phase_function(time):
    return 0.0


'''
Function build_time_list(start,end,step)

:param start is the value of the first element to be included in the list
:param end is the upper bound of the list
:param step is the size of the step between each value in the list

:return a list containing times from start to end in increments of step
'''


def build_time_list(start, end, step):
    time_list = []
    while start <= end:
        time_list.append(start)
        start += step
    return time_list

'''
Function generator(times, freq_func, ampl_func, phase_func, out_file)

:param times: a 3-element list of the format [start_time, end_time, step]
:param freq_func: a function declaring how to vary the frequency with time
:param ampl_func: a function declaring how to vary the amplitude with time
:param phase_func: a function declaring how to vary the phase with time

:return a curve object containing the artificial data
'''


def generator(times, freq_func, ampl_func, phase_func):
    dp_list = []
    t_list = build_time_list(times[0], times[1], times[2])
    for time in t_list:
        flux = lc_fit_function(time, freq_func(time), ampl_func(time), phase_func(time))
        dp_list.append(DataPoint(time, flux))
    return Curve(dp_list)


'''
Function run(start_time, end_time, step)

:param start_time is the start time, in seconds, of the data set
:param end_time is the end time, in seconds, of the data set
:param step is the size of each step between start time and end time, in seconds
'''


def run(start_time, end_time, step):
    time_list = [start_time, end_time, step]
    artificial_data = generator(time_list, frequency_func, amplitude_func, phase_function)
    artificial_data.toFile(OUT_FILE)

run(START_DATE * SEC_IN_YEAR, END_DATE * SEC_IN_YEAR, STEP)
print "Done."

