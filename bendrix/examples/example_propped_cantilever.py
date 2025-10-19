from ...bendrix.beam_analysis.beam import Beam
from ...bendrix.beam_analysis.supports import Support
from ...bendrix.loads.loads import UniformDistributedLoad

beam = Beam(length=4000, beam_type='propped_cantilever')
beam.add_support(Support(position=0, type='fixed'))
beam.add_support(Support(position=4000, type='roller'))
beam.add_load(UniformDistributedLoad(magnitude=1.0, start=0, end=4000))
reactions = beam.calculate_reactions()
print("Propped Cantilever Reactions:")
for key, val in reactions.items():
    print(f"{key}: {val}")
beam.plot_diagrams()
beam.export_sf_bm_to_csv('propped_cantilever.csv')