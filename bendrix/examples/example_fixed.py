from ...bendrix.beam_analysis.beam import Beam
from ...bendrix.beam_analysis.supports import Support
from ...bendrix.loads.loads import UniformDistributedLoad

beam = Beam(length=6000, beam_type='fixed')
beam.add_support(Support(position=0, type='fixed'))
beam.add_support(Support(position=6000, type='fixed'))
beam.add_load(UniformDistributedLoad(magnitude=0.5, start=0, end=6000))
reactions = beam.calculate_reactions()
print("Fixed Beam Reactions:")
for key, val in reactions.items():
    print(f"{key}: {val}")
beam.plot_diagrams()
beam.export_sf_bm_to_csv('fixed.csv')