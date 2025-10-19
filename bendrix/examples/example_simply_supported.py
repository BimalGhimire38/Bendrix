import os
import sys

# Ensure project root (parent of the 'bendrix' package) is on sys.path when executed directly
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from bendrix.beam_analysis.beam import Beam
from bendrix.beam_analysis.supports import Support
from bendrix.loads.loads import PointLoad, UniformDistributedLoad


def main(save_dir=None):
    beam = Beam(length=5000, beam_type='simply_supported')
    beam.add_support(Support(position=0, type='pinned'))
    beam.add_support(Support(position=5000, type='roller'))
    beam.add_load(PointLoad(magnitude=1000, position=2000))
    beam.add_load(UniformDistributedLoad(magnitude=0.2, start=0, end=5000))
    reactions = beam.calculate_reactions()
    print("Simply Supported Reactions:")
    for key, val in reactions.items():
        print(f"{key}: {val}")
    if save_dir is None:
        save_dir = os.path.join(os.path.dirname(__file__), '')
    beam.plot_diagrams(save_path=save_dir, show=False)
    csv_path = os.path.join(save_dir, 'simply_supported.csv')
    beam.export_sf_bm_to_csv(csv_path)


if __name__ == '__main__':
    main()