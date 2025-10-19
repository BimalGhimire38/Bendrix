import numpy as np
from .supports import Support
from ..loads.loads import PointLoad, UniformDistributedLoad, UniformVaryingLoad, MomentLoad
from ..utils.unit_conversion import UnitConversion

class Beam:
    def __init__(self, length, beam_type, length_unit='mm'):
        self.length = UnitConversion.convert(length, length_unit, 'mm')  # Internal: mm
        self.beam_type = beam_type
        self.supports = []
        self.loads = []

    def add_support(self, support):
        if not isinstance(support, Support):
            raise ValueError("Must add a Support instance")
        if not (0 <= support.position <= self.length):
            raise ValueError("Support position must be within beam length")
        self.supports.append(support)

    def add_load(self, load):
        if not isinstance(load, (PointLoad, UniformDistributedLoad, UniformVaryingLoad, MomentLoad)):
            raise ValueError("Must add a valid Load instance")
        self.loads.append(load)

    def calculate_reactions(self):
        if self.beam_type == 'simply_supported':
            return self._calc_simply_supported()
        elif self.beam_type == 'cantilever':
            return self._calc_cantilever()
        elif self.beam_type == 'overhanging':
            return self._calc_overhanging()
        elif self.beam_type == 'fixed':
            return self._calc_fixed()  # Indeterminate; uses simplified formula for uniform load
        elif self.beam_type == 'continuous':
            raise NotImplementedError("Continuous beams require advanced methods (e.g., moment distribution)")
        elif self.beam_type == 'propped_cantilever':
            return self._calc_propped_cantilever()  # Indeterminate; simplified
        else:
            raise ValueError(f"Unsupported beam type: {self.beam_type}")

    def _calc_simply_supported(self):
        # Assume two supports: left pinned at 0, right roller at length
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[1].position != self.length:
            raise ValueError("Simply supported requires supports at 0 and length")
        A, B = self.supports  # A: pinned, B: roller

        # Total vertical force (downward positive)
        total_force = sum(load.get_total_force() for load in self.loads)

        # Sum moments about A (clockwise positive)
        sum_ma = 0.0
        for load in self.loads:
            sum_ma += load.get_moment_about(0)

        # Reactions
        rb = -sum_ma / self.length  # N
        ra = total_force - rb  # Adjust sign if loads downward positive

        A.reaction_force = ra
        B.reaction_force = rb

        return {
            f"Support at {A.position} mm": f"{A.reaction_force} N",
            f"Support at {B.position} mm": f"{B.reaction_force} N"
        }

    def _calc_cantilever(self):
        # Assume fixed at 0, free at length
        if len(self.supports) != 1 or self.supports[0].position != 0 or self.supports[0].type != 'fixed':
            raise ValueError("Cantilever requires fixed support at 0")
        fixed = self.supports[0]

        # Total vertical force
        total_force = sum(load.get_total_force() for load in self.loads)

        # Sum moments about fixed end
        sum_m = sum(load.get_moment_about(0) for load in self.loads)

        fixed.reaction_force = total_force
        fixed.reaction_moment = -sum_m  # N*mm

        return {
            f"Support at {fixed.position} mm": f"Force: {fixed.reaction_force} N, Moment: {fixed.reaction_moment} N*mm"
        }

    def _calc_overhanging(self):
        # Assume supports at 0 and some internal point, overhang beyond
        if len(self.supports) != 2:
            raise ValueError("Overhanging requires two supports")
        self.supports.sort(key=lambda s: s.position)
        A, B = self.supports  # A at left, B at right, overhang beyond B

        total_force = sum(load.get_total_force() for load in self.loads)
        sum_ma = sum(load.get_moment_about(A.position) for load in self.loads)
        span_ab = B.position - A.position

        rb = -sum_ma / span_ab
        ra = total_force - rb

        A.reaction_force = ra
        B.reaction_force = rb

        return {
            f"Support at {A.position} mm": f"{A.reaction_force} N",
            f"Support at {B.position} mm": f"{B.reaction_force} N"
        }

    def _calc_fixed(self):
        # Indeterminate; assume uniform distributed load only, use standard formula
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[1].position != self.length:
            raise ValueError("Fixed beam requires fixed supports at 0 and length")
        if len(self.loads) != 1 or not isinstance(self.loads[0], UniformDistributedLoad):
            raise ValueError("Fixed beam calculation simplified for single UDL only")

        A, B = self.supports
        udl = self.loads[0]
        w = udl.magnitude  # N/mm
        L = self.length

        ra = rb = (w * L) / 2
        ma = mb = - (w * L ** 2) / 12  # N*mm

        A.reaction_force = ra
        A.reaction_moment = ma
        B.reaction_force = rb
        B.reaction_moment = mb

        return {
            f"Support at {A.position} mm": f"Force: {ra} N, Moment: {ma} N*mm",
            f"Support at {B.position} mm": f"Force: {rb} N, Moment: {mb} N*mm"
        }

    def _calc_propped_cantilever(self):
        # Assume fixed at 0, propped (roller) at length; indeterminate, simplified for UDL
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[0].type != 'fixed' or self.supports[1].type != 'roller':
            raise ValueError("Propped cantilever: fixed at 0, roller at length")
        if len(self.loads) != 1 or not isinstance(self.loads[0], UniformDistributedLoad):
            raise ValueError("Propped cantilever simplified for single UDL")

        fixed, prop = self.supports
        udl = self.loads[0]
        w = udl.magnitude  # N/mm
        L = self.length

        rp = (5 * w * L) / 8  # Prop reaction
        rf = (w * L) - rp
        mf = - (w * L ** 2) / 8  # Fixed moment

        fixed.reaction_force = rf
        fixed.reaction_moment = mf
        prop.reaction_force = rp

        return {
            f"Support at {fixed.position} mm": f"Force: {rf} N, Moment: {mf} N*mm",
            f"Support at {prop.position} mm": f"{rp} N"
        }