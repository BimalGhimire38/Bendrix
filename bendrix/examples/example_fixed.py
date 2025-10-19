import os
import sys

# Ensure project root (parent of the 'bendrix' package) is on sys.path when executed directly
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from bendrix.beam_analysis.beam import Beam
from bendrix.beam_analysis.supports import Support
from bendrix.loads.loads import UniformDistributedLoad


def main(save_dir=None):
    beam = Beam(length=6000, beam_type='fixed')
    beam.add_support(Support(position=0, type='fixed'))
    beam.add_support(Support(position=6000, type='fixed'))
    beam.add_load(UniformDistributedLoad(magnitude=0.5, start=0, end=6000))
    reactions = beam.calculate_reactions()
    print("Fixed Beam Reactions:")
    for key, val in reactions.items():
        print(f"{key}: {val}")
    if save_dir is None:
        save_dir = os.path.join(os.path.dirname(__file__), '')
    beam.plot_diagrams(save_path=save_dir, show=False)
    csv_path = os.path.join(save_dir, 'fixed.csv')
    beam.export_sf_bm_to_csv(csv_path)


if __name__ == '__main__':
    main()