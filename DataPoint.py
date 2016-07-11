__author__ = 'sean_moorhead'

class DataPoint(object):

    def __init__(self, x_val = None, y_val = None, z_val = None):
        if x_val is None:
            x_val = 0.0
        if y_val is None:
            y_val = 0.0
        if z_val is None:
            z_val = 0.0
        self.x = float(x_val)
        self.y = float(y_val)
        self.z = float(z_val)

    def set_x(self, x_val):
        self.x = float(x_val)

    def set_y(self, y_val):
        self.y = float(y_val)

    def set_z(self, z_val):
        self.z = float(z_val)

    def set_pt(self, x_val = 0.0, y_val = 0.0, z_val = 0.0):
        self.x = float(x_val)
        self.y = float(y_val)
        self.z = float(z_val)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def __str__(self):
        return "x = " + str(self.x) + ", y = " + str(self.y) + ", z = " + str(self.z)

    def clean_str(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z)
