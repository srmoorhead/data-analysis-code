import numpy as np
from DataPoint import *
from Curve import *

__author__ = 'sean_moorhead'

# global variables
INFILE = 'inputFile.dat'
OUTFILE = 'outputFile.dat'
OUTPUT_STEP = 0.5
DEG = 2
SEC_IN_YEAR = 31557600  # 1 year = 365.25 days,  1 day = 24 hours

def pdot_fit(xarr, yarr, degree):
    return np.polyfit(xarr, yarr, degree)

def build_curve(lowx, hix, step, coef):
    points = []
    y_eq = np.poly1d(coef)
    while lowx <= hix:
        pt = DataPoint(lowx, y_eq(lowx))
        points.append(pt)
        lowx += step
    fit_curve = Curve(points)
    return fit_curve

def read_pdot(f_string):
    xs = []
    ys = []
    with open(f_string, 'r') as data:
        pdot_list = data.read().splitlines()
        for pdot in pdot_list:
            columns = pdot.split()
            if len(columns) != 1:
                xs.append(float(columns[0]))
                ys.append(float(columns[1]))
    return xs, ys

def run():
    x_list, y_list = read_pdot(INFILE)
    coef_arr = pdot_fit(np.array(x_list), np.array(y_list), DEG)

    #fit_curve = build_curve(x_list[0], x_list[-1], OUTPUT_STEP, coef_arr)
    fit_curve = build_curve(x_list[0], 2015, OUTPUT_STEP, coef_arr)
    fit_curve.toFile(OUTFILE)
    print "Curve written to: " + OUTFILE

    if DEG == 1:
        print "Pdot = " + str(coef_arr[0] / SEC_IN_YEAR) + " s s^-1"
    elif DEG == 2:
        print "d/dt dP/dt = " + str(2 * coef_arr[0] / SEC_IN_YEAR) + " s s^-2"

run()
print "Done."
