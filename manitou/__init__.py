from mpd import *

class Manitou(object):
    def __init__(self, structure, **kwargs):
        self.structure = structure
        self.settings = kwargs
        
    def render(self):
        result = MPD()
        return result.xml
        
    def save(self, target):
        path = str(target)
        with open(path, w) as f:
            f.write(self.render())
