# imports
from __future__ import division

__author__ = 'sean_moorhead'

class Mode(object):

    def __get_period(self):

        percentError = (self.frequency[1] / self.frequency[0]) * 100
        period = 1 / self.frequency[0]
        periodErr = (percentError / 100) * period

        return [period, periodErr]

    def __init__(self, frequency, amplitude, phase, fErr = 0.0, aErr = 0.0, phErr = 0.0, fNum = -1):
        self.frequency = [frequency, fErr]
        self.period = self.__get_period()
        self.amplitude = [amplitude, aErr]
        self.phase = [phase, phErr]
        self.fNum = fNum

    def set_fErr(self, val):
        self.frequency[1] = val
        self.period = self.__get_period()

    def set_aErr(self, val):
        self.amplitude[1] = val

    def set_phErr(self, val):
        self.phase[1] = val

    def get_frequency(self):
        return self.frequency[0]

    def get_fErr(self):
        return self.frequency[1]

    def get_amplitude(self):
        return self.amplitude[0]

    def get_aErr(self):
        return self.amplitude[1]

    def get_phase(self):
        return self.phase[0]

    def get_phErr(self):
        return self.phase[1]

    def get_period(self):
        return self.period[0]

    def get_perErr(self):
        return self.period[1]

    def get_fNum(self):
        return self.fNum

    def get_mode(self):
        return [self.frequency, self.amplitude, self.phase]

    def f_str(self, inclErr):
        if inclErr:
            return str(self.frequency[0]) + ' +/- ' + str(self.frequency[1])
        else:
            return str(self.frequency[0])

    def a_str(self, inclErr):
        if inclErr:
            return str(self.amplitude[0]) + ' +/- ' + str(self.amplitude[1])
        else:
            return str(self.amplitude[0])

    def ph_str(self, inclErr):
        if inclErr:
            return str(self.phase[0]) + ' +/- ' + str(self.phase[1])
        else:
            return str(self.phase[0])

    def per_str(self, inclErr):
        if inclErr:
            return str(self.period[0]) + ' +/- ' + str(self.period[1])

    def __str__(self):
        return str(self.fNum) + '\t' + self.f_str(True) + '\t' + self.per_str(True) + '\t' + self.a_str(True) + \
               '\t' + self.ph_str(True)

    def str_no_err(self):
        return self.f_str(False) + "\t" + self.per_str(False) + '\t' + self.a_str(False) + "\t" + self.ph_str(False)
