__author__ = 'sean_moorhead'

from Mode import *
from math import sqrt

# global variables
# largely for convenience
FREQ_FILE_STRING = '../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/2008_frequencies.per'
ERR_FILE_STRING = '../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/2008_frequencies.err'
SAVE_DATA = True
MODE_OUT_FILE_STRING = '../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/2008_modes.dat'
COMBOS_OUT_FILE_STRING = '../PG1159-035/pg1159lcs/2008lcs/moorhead/trimmed/2008_combos.dat'
SEARCH_RANGE = range(1, 5)  # range(1, 11) will search from 1 through 10

'''
Function:  readIn(freqsPath, errsPath)

Read in the files to lists of the lines in the files.
Trim the errsPath data to only include the relevant frequency information.

Return both lists.
'''
def readIn(freqsPath, errsPath):

    errsFile = open(errsPath, "r")
    errs = errsFile.read()
    startIndex = errs.index("F1")
    try:
        endIndex = errs.index("Results for")
    except ValueError:
        endIndex = len(errs)


    trimmed = errs[startIndex : endIndex]
    trimmed = trimmed.splitlines()

    freqs = open(freqsPath, "r")
    freqsLines = freqs.readlines()

    freqs.close()
    errsFile.close()

    return freqsLines, trimmed

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
Function:  build_mode_list(freqs, errs)

Takes two lists:  a list of the lines in a frequency file and a list of the lines in an error file.
From each frequency and corresponding error, create a new Mode object containing all the info for that mode.
Combine all modes into an array in the same order they were in from the input file.

Return a list of Mode objects, each one representing a mode in the input files.
'''
def build_mode_list(freqs, errs):

    mode_list = []

    for i, line in enumerate(freqs):
        f_line_elements = line.split()
        e_line_elements = errs[i].split()

        f_line_elements = list_to_float(f_line_elements)
        e_line_elements = list_to_float(e_line_elements)

        mode = Mode(f_line_elements[1], f_line_elements[2], f_line_elements[3], e_line_elements[1], e_line_elements[2],
                    e_line_elements[3], f_line_elements[0])

        mode_list.append(mode)

    return mode_list

'''
Function: ascending(mode_list)

A basic insertion sort.

Return sorted mode_list
'''
def ascending(mode_list):
    listlen = len(mode_list)
    i = 1
    while i < listlen:
        f = mode_list[i]
        j = i
        while j > 0 and mode_list[j - 1].get_frequency() > f.get_frequency():
            mode_list[j] = mode_list[j - 1]
            j = j - 1
        mode_list[j] = f
        i += 1

    return mode_list


'''
Function: prop_err(a, mode1, b, mode2)

Propagate the error through a linear combination.

Return the propagated error as a float.
'''
def prop_err(a, mode1, b, mode2):
    return sqrt(((a * mode1.get_fErr()) ** 2) + ((b * mode2.get_fErr()) ** 2))

'''
Function:  overlaps(mode, freq, fErr)

If the mode +/- errors overlaps with freq +/- fErr, returns True.
Else, returns False.
'''
def overlaps(mode, freq, fErr):
    m_upper = mode.get_frequency() + mode.get_fErr()
    m_lower = mode.get_frequency() - mode.get_fErr()
    f_upper = freq + fErr
    f_lower = freq - fErr

    if m_lower <= f_upper and m_upper >= f_lower:
        return True
    else:
        return False


'''
Function:  search_for_linear_combinations(mode_list, searchRange)

Take a list of modes and search it for linear combinations.
Vary a and b of the function:  aX + bY = c in the range of searchRange.

Return a list of found combinations of the type
                    a * Mode1 + b * Mode2 = Mode3
                                        in the following format:

    a Mode1 b Mode2 Mode3
    a Mode1 b Mode2 Mode3
    ...
'''
def search_for_linear_combinations(mode_list, searchRange):
    mode_list = ascending(mode_list)
    combinations = []

    for i, mode1 in enumerate(mode_list):
        for j, mode2 in enumerate(mode_list[i:]):
            for a in searchRange:
                for b in searchRange:
                    combo_f = (a * mode1.get_frequency()) + (b * mode2.get_frequency())
                    combo_fErr = prop_err(a, mode1, b, mode2)

                    for mode3 in mode_list[j:]:
                        if overlaps(mode3, combo_f, combo_fErr):
                            combinations.append([a, mode1, b, mode2, mode3])

    return combinations

'''
Function:   mode_list_to_file(mode_list, outfile_path)

Takes a list of modes and prints them to a file in their standard string output
'''
def mode_list_to_file(mode_list, outfile_path):
    fw = open(outfile_path, 'w')
    fw.write('F#\tFrequency +/- FreqErr\tPeriod +\- PerErr\tAmplitude +\- AmplErr\tPhase +\- PhaseErr\n')  # header
    for mode in mode_list:
        fw.write(str(mode) + '\n')
    fw.close()

'''
Function:   get_df(combo)

Takes a combination set and returns a string that is the value of f3 - ((a * f1) +  (b * f2))
'''
def get_df(combo):
    f1 = combo[0] * combo[1].get_frequency()
    f2 = combo[2] * combo[3].get_frequency()
    f3 = combo[4].get_frequency()

    return f3 - (f1 + f2)

'''
Function:   combo_list_to_file(combo_list, outfile_path)

Takes a list of combinations and prints them to a file in mode standard string output
'''
def combo_list_to_file(combo_list, outfile_path):
    fw = open(outfile_path, 'w')
    PM = ' +/- '
    for num, combo in enumerate(combo_list):
        fw.write('C' + str(num + 1) + '\t')
        fw.write(str(combo[0]) + '\t')
        fw.write(str(combo[1].get_frequency()) + PM + str(combo[1].get_fErr()) + '\t')
        fw.write(str(combo[2]) + '\t')
        fw.write(str(combo[3].get_frequency()) + PM + str(combo[3].get_fErr()) + '\t')
        fw.write(str(combo[4].get_frequency()) + PM + str(combo[4].get_fErr()) + '\t')
        fw.write(str(get_df(combo)))
        fw.write('\n')
    fw.close()

'''
Function:  run(freqFile, errFile, save)

Runs the linear combination search.
If save is True, saves the files in global variable paths.
'''
def run(freqFile, errFile, save):

    fs, es = readIn(freqFile, errFile)
    print "Files read."

    modes = build_mode_list(fs, es)
    print "Modes constructed."

    if save:
        mode_list_to_file(modes, MODE_OUT_FILE_STRING)
        print "Modes saved."

    combos = search_for_linear_combinations(modes, SEARCH_RANGE)
    print "Search complete."

    if save:
        combo_list_to_file(combos, COMBOS_OUT_FILE_STRING)
        print "Combinations saved."

    print "Done."

run(FREQ_FILE_STRING, ERR_FILE_STRING, SAVE_DATA)
