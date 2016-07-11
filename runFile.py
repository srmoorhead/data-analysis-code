from BasicIO import lc_read_in, freq_read_in, build_fit

# from this file, all other programs are called.  This is where all runtime editing should occur.

__author__ = 'sean_moorhead'

# global variables
F_FILE = "../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/halves/top23_trimmed_2o2.per"
LC_FILE = "../PG1159-035/pg1159lcs/2008lcs/lightcurves/pg1159xcov27_trimmed_2o2.dat"
OUT_FILE = "../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/halves/top23_trimmed_2o2_fitcurve.dat"

def build_curve_from_fit_data():
    lc = lc_read_in(LC_FILE)
    f = freq_read_in(F_FILE)
    fit = build_fit(f)
    zeropt = lc.avg_y()
    fitdata = fit.build_curve(zeropt, lc.get_x_list())
    fitdata.toFile(OUT_FILE)

build_curve_from_fit_data()