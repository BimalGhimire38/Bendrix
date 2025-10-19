from bendrix.beam_analysis.beam import Beam
from bendrix.beam_analysis.supports import Support
from bendrix.loads.loads import PointLoad, UniformDistributedLoad, UniformVaryingLoad, MomentLoad

def main():
    # Example: Simply supported beam
    beam = Beam(length=5000, beam_type='simply_supported', length_unit='mm')  # 5m = 5000mm
    beam.add_support(Support(position=0, type='pinned'))
    beam.add_support(Support(position=5000, type='roller'))
    beam.add_load(PointLoad(magnitude=1000, position=2000))  # 1000N at 2000mm
    beam.add_load(UniformDistributedLoad(magnitude=0.5, start=1000, end=4000))  # 0.5 N/mm from 1000-4000mm

    reactions = beam.calculate_reactions()
    print("Simply Supported Reactions:")
    for key, val in reactions.items():
        print(f"{key}: {val}")

    # Example: Cantilever
    cantilever = Beam(length=3000, beam_type='cantilever')
    cantilever.add_support(Support(position=0, type='fixed'))
    cantilever.add_load(PointLoad(magnitude=500, position=1500))
    reactions = cantilever.calculate_reactions()
    print("\nCantilever Reactions:")
    for key, val in reactions.items():
        print(f"{key}: {val}")

    # Add more examples as needed

if __name__ == "__main__":
    main()