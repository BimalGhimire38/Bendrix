class Loads:
    def __init__(self):
        pass

    def point_load(self,magnitude,position):
        self.magnitude = magnitude
        self.position = position 
        return self.magnitude, self.position
    
    def udl(self,magnitude,start,end):
        self.magnitude = magnitude
        self.start = start
        self.end = end
        return self.magnitude, self.start, self.end