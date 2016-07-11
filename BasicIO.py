from Fit import *
from Mode import *

__author__ = 'sean_moorhead'

'''
Function:  readIn(freqsPath, errsPath)

Read in the files to lists of the lines in the files.
Trim the errsPath data to only include the relevant frequency information.

Return both lists.
'''
def freq_read_in(freqsPath, errsPath = ""):
    have_error = True
    if errsPath is "":
        have_error = False

    trimmed = []
    if have_error:
        errsFile = open(errsPath, "r")
        errs = errsFile.read()
        startIndex = errs.index("F1")

        trimmed = errs[startIndex:]
        trimmed = trimmed.splitlines()

        errsFile.close()

    freqs = open(freqsPath, "r")
    freqsLines = freqs.readlines()

    freqs.close()

    if have_error:
        return freqsLines, trimmed
    return freqsLines

'''
Function: to_float(string)

Take a string object that is a number and return that object as a float.
Handles cases of numbers such as:  0.000444924e-5  and  111.209481e+12

Return the float of the number represented in the string.
'''
def to_float(string):
    if 'F' in string:
        return string

    if 'e' in string:
        valExp = string.split('e')
        num = valExp[0]
        exp = valExp[1]
        if '+' in exp:
            exp = exp[1:]
        return float(num) * (10 ** float(exp))

    return float(string)

'''
Function:  list_to_float(data)

Calls the to_float(string) function on every item in a list.

Returns a list containing all objects within as floats.
'''
def list_to_float(data):
    new_list = []
    for item in data:
        new_list.append(to_float(item))
    return new_list

'''
Function:  build_fit(freqs, errs)

Takes two lists:  a list of the lines in a frequency file and a list of the lines in an error file.
From each frequency and corresponding error, create a new Mode object containing all the info for that mode.
Combine all modes into a fit.

Return a Fit object, representing all modes in the input files.
'''
def build_fit(freqs, errs = None):

    mode_list = Fit()

    if errs is None:
        for line in freqs:
            f_line_elements = list_to_float(line.split())

            mode = Mode(f_line_elements[1], f_line_elements[2], f_line_elements[3])
            mode_list.add_mode(mode)
    else:
        for i, line in enumerate(freqs):
            f_line_elements = line.split()
            e_line_elements = errs[i].split()

            f_line_elements = list_to_float(f_line_elements)
            e_line_elements = list_to_float(e_line_elements)

            mode = Mode(f_line_elements[1], f_line_elements[2], f_line_elements[3], e_line_elements[1], e_line_elements[2],
                        e_line_elements[3])

            mode_list.add_mode(mode)

    return mode_list

def lc_read_in(lc_file):
    pt_list = []
    with open(lc_file, 'r') as lcf:
        lc_list = lcf.read().splitlines()

        for line in lc_list:
            line_elements = line.split()
            point = DataPoint(line_elements[0], line_elements[1])
            pt_list.append(point)
    lc = Curve()

    lc.add_set(pt_list)

    return lc
