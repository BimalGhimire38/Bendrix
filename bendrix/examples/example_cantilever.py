from ...bendrix.beam_analysis.beam import Beam
from ...bendrix.beam_analysis.supports import Support
from ...bendrix.loads.loads import PointLoad, MomentLoad

beam = Beam(length=3000, beam_type='cantilever')
beam.add_support(Support(position=0, type='fixed'))
beam.add_load(PointLoad(magnitude=500, position=1500))
beam.add_load(MomentLoad(magnitude=1000, position=3000))
reactions = beam.calculate_reactions()
print("Cantilever Reactions:")
for key, val in reactions.items():
    print(f"{key}: {val}")
beam.plot_diagrams()
beam.export_sf_bm_to_csv('cantilever.csv')