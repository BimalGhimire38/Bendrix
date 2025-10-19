from abc import ABC, abstractmethod
from ..utils.unit_conversion import UnitConversion

class Load(ABC):
    @abstractmethod
    def get_total_force(self):
        pass

    @abstractmethod
    def get_moment_about(self, ref_point):
        pass

class PointLoad(Load):
    def __init__(self, magnitude, position, cw_angle_to_left=0, magnitude_unit='N', position_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N')
        self.position = UnitConversion.convert(position, position_unit, 'mm')
        self.cw_angle_to_left = cw_angle_to_left  # For future: resolve components, but simple: assume vertical

    def get_total_force(self):
        return self.magnitude  # Vertical component

    def get_moment_about(self, ref_point):
        distance = self.position - ref_point
        return self.magnitude * distance  # Clockwise positive

class UniformDistributedLoad(Load):
    def __init__(self, magnitude, start, end, magnitude_unit='N/mm', start_unit='mm', end_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N/mm')  # Per mm
        self.start = UnitConversion.convert(start, start_unit, 'mm')
        self.end = UnitConversion.convert(end, end_unit, 'mm')

    def get_total_force(self):
        return self.magnitude * (self.end - self.start)

    def get_moment_about(self, ref_point):
        centroid = (self.start + self.end) / 2
        distance = centroid - ref_point
        return self.get_total_force() * distance

class UniformVaryingLoad(Load):
    def __init__(self, start_magnitude, end_magnitude, start, end, mag_unit='N/mm', start_unit='mm', end_unit='mm'):
        self.start_magnitude = UnitConversion.convert(start_magnitude, mag_unit, 'N/mm')
        self.end_magnitude = UnitConversion.convert(end_magnitude, mag_unit, 'N/mm')
        self.start = UnitConversion.convert(start, start_unit, 'mm')
        self.end = UnitConversion.convert(end, end_unit, 'mm')

    def get_total_force(self):
        # Trapezoidal: average magnitude * length
        avg_mag = (self.start_magnitude + self.end_magnitude) / 2
        return avg_mag * (self.end - self.start)

    def get_moment_about(self, ref_point):
        # Centroid location from start: (2*end_mag + start_mag)/(3*(start_mag + end_mag)) * length
        length = self.end - self.start
        if self.start_magnitude == self.end_magnitude:
            centroid_from_start = length / 2
        else:
            centroid_from_start = length * (2 * self.end_magnitude + self.start_magnitude) / (3 * (self.start_magnitude + self.end_magnitude))
        centroid = self.start + centroid_from_start
        distance = centroid - ref_point
        return self.get_total_force() * distance

class MomentLoad(Load):
    def __init__(self, magnitude, position, magnitude_unit='N*mm', position_unit='mm'):
        self.magnitude = UnitConversion.convert(magnitude, magnitude_unit, 'N*mm')
        self.position = UnitConversion.convert(position, position_unit, 'mm')

    def get_total_force(self):
        return 0.0  # No vertical force

    def get_moment_about(self, ref_point):
        if ref_point == self.position:
            return self.magnitude
        return 0.0  # Moment only at point, but for equilibrium, it contributes fully if ref not at point? Wait, moments are absolute, but in beam, it's local.
        # Simplified: for reaction calc, if ref is not at load, still contributes, but actually moments are additive regardless.
        # Correction: pure moment contributes to moment eq regardless of ref, but changes sign/distance? No, pure moment is distance-independent in sum M.
        # For equilibrium, sum M = sum (forces*d) + sum moments.
        # So pure moment adds directly to sum M, regardless of ref_point.
        return self.magnitude