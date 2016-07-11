from BasicIO import lc_read_in, freq_read_in, build_fit

# from this file, all other programs are called.  This is where all runtime editing should occur.

__author__ = 'sean_moorhead'

# global variables
F_FILE = "frequenciesFile.per"
LC_FILE = "lightcurveFile.dat"
OUT_FILE = "outputFile.dat"

def build_curve_from_fit_data():
    lc = lc_read_in(LC_FILE)
    f = freq_read_in(F_FILE)
    fit = build_fit(f)
    zeropt = lc.avg_y()
    fitdata = fit.build_curve(zeropt, lc.get_x_list())
    fitdata.toFile(OUT_FILE)

build_curve_from_fit_data()