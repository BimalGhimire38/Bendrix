# Define load types
class Loads:
    def __init__(self):
        pass

    def point_load(self, magnitude, cw_angle_to_left, position):
        self.magnitude = magnitude
        self.position = position
        self.cw_angle_to_left = cw_angle_to_left
        return self.magnitude, self.position

    def udl(self, magnitude, start, end):
        self.magnitude = magnitude
        self.start = start
        self.end = end
        return self.magnitude, self.start, self.end

    def uvl(self, start_magnitude, end):
        self.start_magnitude = start_magnitude
        self.end = end
        return self.start_magnitude, self.end

    def moment(self, magnitude, position):
        self.magnitude = magnitude
        self.position = position
        return self.magnitude, self.position