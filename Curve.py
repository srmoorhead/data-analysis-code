from __future__ import division

__author__ = 'sean_moorhead'

class Curve:

    def __init__(self, list_of_points = None):
        if list_of_points is None:
            list_of_points = []
        self.curve_list = sorted(list_of_points, key = lambda datpt: datpt.x)

    def add_point(self, point):
        self.curve_list.append(point)
        self.curve_list.sort(key = lambda datpt: datpt.x)

    def add_set(self, list_of_points):
        for point in list_of_points:
            self.curve_list.append(point)
        self.curve_list.sort(key = lambda datpt: datpt.x)

    def __str__(self):
        return_str = ""
        for point in self.curve_list:
            return_str += point.clean_str() + '\n'
        return return_str

    def __repr__(self):
        return 'Curve:  Size=%s, Start=%s, End=%s' % (self.curve_list.len(), self.curve_list[0].get_x(),
                                                      self.curve_list[-1].get_x())

    def get_len(self):
        return self.curve_list.len()

    def get_start_x(self):
        return self.curve_list[0].get_x()

    def get_end_x(self):
        return self.curve_list[-1].get_x()

    def get_x_list(self):
        return_list = []
        for point in self.curve_list:
            return_list.append(point.x)
        return return_list

    def get_y_list(self):
        return_list = []
        for point in self.curve_list:
            return_list.append(point.y)
        return return_list

    def get_z_list(self):
        return_list = []
        for point in self.curve_list:
            return_list.append(point.z)
        return return_list

    def subset(self, xStart, xEnd):
        stI = 0
        while self.curve_list[stI].x < xStart:
            stI += 1

        enI = stI
        while self.curve_list[enI].x < xEnd:
            enI += 1

        return Curve(self.curve_list[stI, enI])

    def toFile(self, fileString):
        with open(fileString, 'w') as f:
            f.write(str(self))

    def combine(self, otherCurve):
        self.add_set(otherCurve.list_of_points)

    def __getitem__(self, index):
        return self.curve_list[index]

    def avg_y(self):
        sum = 0.0
        count = 0.0
        for point in self.curve_list:
            sum += point.y
            count += 1
        return sum / count

    def avg_x(self):
        sum = 0.0
        count = 0.0
        for point in self.curve_list:
            sum += point.x
            count += 1
        return sum / count

    def avg_z(self):
        sum = 0.0
        count = 0.0
        for point in self.curve_list:
            sum += point.z
            count += 1
        return sum / count
