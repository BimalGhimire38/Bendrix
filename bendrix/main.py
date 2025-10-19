# Entry point to run the beam analysis
from ..bendrix.beam_analysis.beam import Beam
from ..bendrix.beam_analysis.supports import Support
from ..bendrix.loads.loads import PointLoad, UniformDistributedLoad

def main():
    # Run a simple example
    beam = Beam(length=5000, beam_type='simply_supported')
    beam.add_support(Support(position=0, type='pinned'))
    beam.add_support(Support(position=5000, type='roller'))
    beam.add_load(PointLoad(magnitude=1000, position=2000))
    beam.add_load(UniformDistributedLoad(magnitude=0.5, start=1000, end=4000))
    reactions = beam.calculate_reactions()
    print("Reactions:")
    for key, val in reactions.items():
        print(f"{key}: {val}")
    beam.plot_diagrams()
    beam.export_sf_bm_to_csv('example.csv')

if __name__ == "__main__":
    main()