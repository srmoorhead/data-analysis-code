from p_dotFit import pdot_fit as adot_fit, build_curve
import numpy as np

__author__ = 'sean_moorhead'

# global variables
INFILE = 'infilename.dat'
OUTFILE = 'outfilename.dat'
OUTPUT_STEP = 1
DEG = 2
SEC_IN_YEAR = 31557600  # 1 year = 365.25 days,  1 day = 24 hours

def read_adot(a_string):
    xs = []
    ys = []
    with open(a_string, 'r') as data:
        pdot_list = data.read().splitlines()
        for pdot in pdot_list:
            columns = pdot.split()
            if len(columns) != 1:
                xs.append(float(columns[0]))
                ys.append(float(columns[3]))
    return xs, ys

def run():
    x_list, y_list = read_adot(INFILE)
    coef_arr = adot_fit(np.array(x_list), np.array(y_list), DEG)

    fit_curve = build_curve(x_list[0], x_list[-1], OUTPUT_STEP, coef_arr)
    fit_curve.toFile(OUTFILE)
    print("Curve written to: " + OUTFILE)

    if DEG == 1:
        print("dA/dt = " + str(coef_arr[0] / SEC_IN_YEAR) + " mma s^-1")
    elif DEG == 2:
        print("d/dt dP/dt = " + str(2 * coef_arr[0] / SEC_IN_YEAR) + " mma s^-2")

run()
print("Done.")