"""
    A simple graph/network based approach for rivers
    
"""
import random
from matplotlib import pyploat as plt

class River:
    def __init__(self, upstream:bool = False):
        self.upstream = upstream        
        pass
    
    def calculateFlow(self):
        pass

    def plot(self):
        pass

if __name__=="__main__":
    riv = River()
    riv.calculateFlow()