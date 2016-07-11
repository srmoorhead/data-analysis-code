from FitFunctions import lc_fit_function
from Curve import Curve
from DataPoint import DataPoint

__author__ = 'sean_moorhead'

class Fit:

    def __init__(self, mode_list = None):
        if mode_list == None:
            mode_list = []
        self.modes = sorted(mode_list, key = lambda m: m.frequency)

    def add_mode(self, mode):
        self.modes.append(mode)
        self.modes.sort(key = lambda m: m.frequency)

    def add_set(self, mode_list):
        for mode in mode_list:
            self.modes.append(mode)
        self.modes.sort(key = lambda m: m.frequency)

    def __str__(self):
        return_str = ""
        for mode in self.modes:
            return_str += str(mode) + '\n'
        return return_str

    def combine(self, otherFit):
        self.add_set(otherFit.modes)

    def __getitem__(self, index):
        return self.modes[index]

    def get_frequencies(self):
        result = []
        for mode in self.modes:
            result.append(mode.frequency)
        return result

    def get_amplitudes(self):
        result = []
        for mode in self.modes:
            result.append(mode.amplitude)
        return result

    def get_phases(self):
        result = []
        for mode in self.modes:
            result.append(mode.phase)
        return result

    def get_periods(self):
        result = []
        for mode in self.modes:
            result.append(mode.period)
        return result

    def subset(self, lowF, highF):
        loI = 0
        while self.modes[loI].frequency < lowF:
            loI += 1

        hiI = loI
        while self.modes[hiI].frequency < highF:
            hiI += 1

        return Fit(self.modes[loI, hiI])

    def toFile(self, fileString):
        with open(fileString, 'w') as f:
            f.write(str(self))

    def build_curve(self, zeropoint, times):
        # Fitting formula:  Z + SUM(amplitude * sin(2pi(frequency * t + phase)))

        fit_list = []

        for time in times:
            fit_sum = 0.0
            for mode in self.modes:
                fit_sum += lc_fit_function(time, mode.get_frequency(), mode.get_amplitude(), mode.get_phase())
            fit_at_time = DataPoint(time, fit_sum - zeropoint)
            fit_list.append(fit_at_time)

        fit_curve = Curve(fit_list)

        return fit_curve