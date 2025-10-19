from abc import ABC, abstractmethod
from ..utils.unit_conversion import UnitConversion

class Load(ABC):
    @abstractmethod
    def get_total_force(self):
        pass

    @abstractmethod
    def get_moment_about(self, ref_point):
        pass

    @abstractmethod
    def get_cumulative_force_up_to(self, x):
        pass

    @abstractmethod
    def get_cumulative_moment_up_to(self, x):
        pass

class PointLoad(Load):
    def __init__(self, magnitude, position, cw_angle_to_left=0, magnitude_unit='N', position_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N')  # Positive down
        self.position = UnitConversion.convert(position, position_unit, 'mm')
        self.cw_angle_to_left = cw_angle_to_left  # Assume vertical for now

    def get_total_force(self):
        return self.magnitude

    def get_moment_about(self, ref_point):
        distance = self.position - ref_point
        return self.magnitude * distance  # Positive clockwise

    def get_cumulative_force_up_to(self, x):
        return self.magnitude if x >= self.position else 0.0

    def get_cumulative_moment_up_to(self, x):
        return 0.0

class UniformDistributedLoad(Load):
    def __init__(self, magnitude, start, end, magnitude_unit='N/mm', start_unit='mm', end_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N/mm')
        self.start = UnitConversion.convert(start, start_unit, 'mm')
        self.end = UnitConversion.convert(end, end_unit, 'mm')

    def get_total_force(self):
        return self.magnitude * (self.end - self.start)

    def get_moment_about(self, ref_point):
        centroid = (self.start + self.end) / 2
        distance = centroid - ref_point
        return self.get_total_force() * distance

    def get_cumulative_force_up_to(self, x):
        if x <= self.start:
            return 0.0
        elif x >= self.end:
            return self.magnitude * (self.end - self.start)
        else:
            return self.magnitude * (x - self.start)

    def get_cumulative_moment_up_to(self, x):
        return 0.0

class UniformVaryingLoad(Load):
    def __init__(self, start_magnitude, end_magnitude, start, end, mag_unit='N/mm', start_unit='mm', end_unit='mm'):
        self.start_magnitude = UnitConversion.convert(start_magnitude, mag_unit, 'N/mm')
        self.end_magnitude = UnitConversion.convert(end_magnitude, mag_unit, 'N/mm')
        self.start = UnitConversion.convert(start, start_unit, 'mm')
        self.end = UnitConversion.convert(end, end_unit, 'mm')

    def get_total_force(self):
        avg = (self.start_magnitude + self.end_magnitude) / 2
        return avg * (self.end - self.start)

    def get_moment_about(self, ref_point):
        length = self.end - self.start
        if self.start_magnitude == self.end_magnitude:
            centroid_from_start = length / 2
        else:
            centroid_from_start = length * (2 * self.end_magnitude + self.start_magnitude) / (3 * (self.start_magnitude + self.end_magnitude))
        centroid = self.start + centroid_from_start
        distance = centroid - ref_point
        return self.get_total_force() * distance

    def get_cumulative_force_up_to(self, x):
        if x <= self.start:
            return 0.0
        length = self.end - self.start
        slope = (self.end_magnitude - self.start_magnitude) / length
        pos = min(x, self.end) - self.start
        return self.start_magnitude * pos + 0.5 * slope * pos ** 2

    def get_cumulative_moment_up_to(self, x):
        return 0.0

class MomentLoad(Load):
    def __init__(self, magnitude, position, magnitude_unit='N*mm', position_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N*mm')
        self.position = UnitConversion.convert(position, position_unit, 'mm')

    def get_total_force(self):
        return 0.0

    def get_moment_about(self, ref_point):
        return self.magnitude

    def get_cumulative_force_up_to(self, x):
        return 0.0

    def get_cumulative_moment_up_to(self, x):
        return self.magnitude if x >= self.position else 0.0