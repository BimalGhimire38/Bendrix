class CalculateReactions:
    def __init__(self,beam_type):
        self.beam_type = beam_type

        if beam_type == 'simply_supported':
            self.calc_simply_supported()

        elif beam_type == 'cantilever':
            self.calc_cantilever()

        elif beam_type == 'fixed':
            self.calc_fixed()

        elif beam_type == 'continuous':
            self.calc_continuous()

        elif beam_type == 'propped_cantilever':
            self.calc_propped_cantilever()

        elif beam_type == 'overhanging':
            self.calc_overhanging()

    def calc_simply_supported(self,length):
        pass
    
    def calc_cantilever(self):
        pass
    def calc_fixed(self):
        pass
    def calc_continuous(self):
        pass
    def calc_propped_cantilever(self):
        pass
    def calc_overhanging(self):
        pass




class SimplySupported:
    def __init__(self,length):
        self.length = length

    
class Cantilever:
    pass

class Fixed:
    pass

class Continuous:
    pass

class Overhanging:
    pass

class ProppedCantilever:
    pass
