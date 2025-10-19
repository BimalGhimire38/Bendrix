import os
import numpy as np
try:
    # Older SciPy versions expose cumtrapz
    from scipy.integrate import cumtrapz
except Exception:
    # Newer SciPy versions provide cumulative_trapezoid (use as a drop-in)
    from scipy.integrate import cumulative_trapezoid as cumtrapz
import matplotlib.pyplot as plt
import csv
from .supports import Support
from ..loads.loads import Load, PointLoad, UniformDistributedLoad, UniformVaryingLoad, MomentLoad
from ..utils.unit_conversion import UnitConversion

class Beam:
    def __init__(self, length, beam_type, length_unit='mm'):
        self.length = UnitConversion.convert(length, length_unit, 'mm')
        self.beam_type = beam_type
        self.supports = []
        self.loads = []
        self.reactions_calculated = False

    def add_support(self, support):
        if not isinstance(support, Support):
            raise ValueError("Must add a Support instance")
        if not (0 <= support.position <= self.length):
            raise ValueError("Support position must be within beam length")
        self.supports.append(support)

    def add_load(self, load):
        if not isinstance(load, Load):
            raise ValueError("Must add a valid Load instance")
        self.loads.append(load)

    def calculate_reactions(self):
        if self.reactions_calculated:
            return self._get_reactions_dict()
        if self.beam_type == 'simply_supported':
            self._calc_simply_supported()
        elif self.beam_type == 'cantilever':
            self._calc_cantilever()
        elif self.beam_type == 'overhanging':
            self._calc_overhanging()
        elif self.beam_type == 'fixed':
            self._calc_fixed()
        elif self.beam_type == 'continuous':
            raise NotImplementedError("Continuous beams require advanced methods (e.g., moment distribution)")
        elif self.beam_type == 'propped_cantilever':
            self._calc_propped_cantilever()
        else:
            raise ValueError(f"Unsupported beam type: {self.beam_type}")
        self.reactions_calculated = True
        return self._get_reactions_dict()

    def _get_reactions_dict(self):
        reactions = {}
        for s in self.supports:
            key = f"Support at {s.position} mm"
            if s.type == 'fixed':
                value = f"Force: {s.reaction_force} N, Moment: {s.reaction_moment} N*mm"
            else:
                value = f"{s.reaction_force} N"
            reactions[key] = value
        return reactions

    def _calc_simply_supported(self):
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[1].position != self.length:
            raise ValueError("Simply supported requires supports at 0 and length")
        self.supports.sort(key=lambda s: s.position)
        A, B = self.supports
        total_force = sum(load.get_total_force() for load in self.loads)
        sum_ma = sum(load.get_moment_about(A.position) for load in self.loads)
        span = B.position - A.position
        B.reaction_force = sum_ma / span
        A.reaction_force = total_force - B.reaction_force

    def _calc_cantilever(self):
        if len(self.supports) != 1 or self.supports[0].position != 0 or self.supports[0].type != 'fixed':
            raise ValueError("Cantilever requires fixed support at 0")
        fixed = self.supports[0]
        total_force = sum(load.get_total_force() for load in self.loads)
        sum_m = sum(load.get_moment_about(0) for load in self.loads)
        fixed.reaction_force = total_force
        fixed.reaction_moment = -sum_m

    def _calc_overhanging(self):
        if len(self.supports) != 2:
            raise ValueError("Overhanging requires two supports")
        self.supports.sort(key=lambda s: s.position)
        A, B = self.supports
        total_force = sum(load.get_total_force() for load in self.loads)
        sum_ma = sum(load.get_moment_about(A.position) for load in self.loads)
        span = B.position - A.position
        B.reaction_force = sum_ma / span
        A.reaction_force = total_force - B.reaction_force

    def _calc_fixed(self):
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[1].position != self.length:
            raise ValueError("Fixed beam requires fixed supports at 0 and length")
        if len(self.loads) != 1 or not isinstance(self.loads[0], UniformDistributedLoad):
            raise ValueError("Fixed beam calculation simplified for single UDL only")
        self.supports.sort(key=lambda s: s.position)
        A, B = self.supports
        udl = self.loads[0]
        w = udl.magnitude
        L = self.length
        A.reaction_force = B.reaction_force = (w * L) / 2
        A.reaction_moment = - (w * L ** 2) / 12
        B.reaction_moment = - (w * L ** 2) / 12

    def _calc_propped_cantilever(self):
        if len(self.supports) != 2 or self.supports[0].position != 0 or self.supports[0].type != 'fixed' or self.supports[1].type != 'roller':
            raise ValueError("Propped cantilever: fixed at 0, roller at length")
        if len(self.loads) != 1 or not isinstance(self.loads[0], UniformDistributedLoad):
            raise ValueError("Propped cantilever simplified for single UDL")
        fixed, prop = self.supports if self.supports[0].position == 0 else self.supports[::-1]
        udl = self.loads[0]
        w = udl.magnitude
        L = self.length
        rp = (3 * w * L) / 8
        rf = (w * L) - rp
        mf = - (w * L ** 2) / 8
        fixed.reaction_force = rf
        fixed.reaction_moment = mf
        prop.reaction_force = rp

    def _compute_shear_at(self, x):
        self.calculate_reactions()
        reac_cum = sum(s.reaction_force for s in self.supports if s.position <= x)
        load_cum = sum(load.get_cumulative_force_up_to(x) for load in self.loads)
        return reac_cum - load_cum

    def plot_diagrams(self, num_points=200, save_path=None, show=True):
        """Plot shear force and bending moment diagrams.

        If save_path is provided, the figure will be saved instead of (or in
        addition to) being shown. save_path may be a directory or a file path.
        The beam type is included in the plot titles and default filenames.
        """
        self.calculate_reactions()
        x = np.linspace(0, self.length, num_points)
        sf = np.array([self._compute_shear_at(xi) for xi in x])
        bm0 = 0
        left_support = min(self.supports, key=lambda s: s.position, default=None)
        if left_support and left_support.position == 0 and left_support.type == 'fixed':
            bm0 = left_support.reaction_moment
        bm = bm0 + cumtrapz(sf, x, initial=0)
        cum_mom = np.array([sum(l.get_cumulative_moment_up_to(xi) for l in self.loads) for xi in x])
        bm += cum_mom
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.plot(x, sf, label='Shear Force')
        # include beam type in titles
        beam_title = (self.beam_type or '').replace('_', ' ').title()
        ax1.set_title(f"{beam_title} — Shear Force Diagram")
        ax1.set_xlabel('Position (mm)')
        ax1.set_ylabel('SF (N)')
        ax1.grid(True)
        ax2.plot(x, bm, label='Bending Moment')
        ax2.set_title(f"{beam_title} — Bending Moment Diagram")
        ax2.set_xlabel('Position (mm)')
        ax2.set_ylabel('BM (N*mm)')
        ax2.grid(True)
        plt.tight_layout()

        if save_path:
            # If a directory is given, construct a default filename
            if os.path.isdir(save_path) or save_path.endswith(os.sep):
                out_dir = save_path
                os.makedirs(out_dir, exist_ok=True)
                safe_name = (self.beam_type or 'beam').replace(' ', '_')
                out_file = os.path.join(out_dir, f"{safe_name}_sf_bm.png")
            else:
                # treat as file path (ensure parent dir exists)
                out_file = save_path
                parent = os.path.dirname(out_file)
                if parent:
                    os.makedirs(parent, exist_ok=True)
            fig.savefig(out_file)
            if not show:
                plt.close(fig)
        else:
            if show:
                plt.show()

    def export_sf_bm_to_csv(self, filename, num_points=20):
        self.calculate_reactions()
        x = np.linspace(0, self.length, num_points)
        sf = np.array([self._compute_shear_at(xi) for xi in x])
        bm0 = 0
        left_support = min(self.supports, key=lambda s: s.position, default=None)
        if left_support and left_support.position == 0 and left_support.type == 'fixed':
            bm0 = left_support.reaction_moment
        bm = bm0 + cumtrapz(sf, x, initial=0)
        cum_mom = np.array([sum(l.get_cumulative_moment_up_to(xi) for l in self.loads) for xi in x])
        bm += cum_mom
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Position (mm)', 'Shear Force (N)', 'Bending Moment (N*mm)'])
            for xi, sfi, bmi in zip(x, sf, bm):
                writer.writerow([xi, sfi, bmi])