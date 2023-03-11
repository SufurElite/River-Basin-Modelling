"""
    A simple graph/network based approach for rivers
    
"""
import random
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as st
import networkx as nx
import math

class River:
    def __init__(self,fractalDim:float, latLength: int = 100, upstream:bool = False):
        self.upstream = upstream      
        # equations for self-similar fractals from Models of Fractal
        # river basins
        self.fractalDim = fractalDim
        self.phi = 2
        self.h = fractalDim/2
        self.tau = 2 - 2/fractalDim
        self.gamma = 2/fractalDim
        self.latLength = latLength
        self.latticeMatrix = np.zeros((self.latLength, self.latLength))        
        self.areaPDF = self.areaProbDensityFunc(self, a=0, b=1)
        self.areaMatrix = np.zeros((self.latLength, self.latLength))
        self.populateLatMatix()

    def getProbability(self, area):
        return self.areaPDF.pdf(area)

    class areaProbDensityFunc(st.rv_continuous):
        def __init__(self, riverModel, a,b):
            super().__init__(a,b)
            self.fractalDim = riverModel.fractalDim
            self.tau = riverModel.tau
            self.phi = riverModel.phi
            self.latLength = riverModel.latLength
            
        def scalingFunction(self,x):
            """ Some scaling function """
            # return math.cosh(x)/np.exp(x)
            # return np.sin(x)/x
            return np.exp(-x)**2
            # return 1-0.8*((np.exp(-0.005*x)-1)/(np.exp(-5.475)-1))
        
        def _pdf(self,x):
            return x**(-self.tau)*self.scalingFunction((x/(self.latLength**self.phi)))

    class upstreamLengthPDF(st.rv_continuous):
        def __init__(self, riverModel, a,b):
            super().__init__(a,b)
            self.fractalDim = riverModel.fractalDim
            self.tau = riverModel.tau
            self.phi = riverModel.phi
            self.latLength = riverModel.latLength
        def _pdf(self,x):
            return x

    def populateLatMatix(self, outlet:tuple[int, int] = (0,0)):
        def dfs(coords, visited, edges,last_s):
            i, j = coords[0], coords[1]
            visited[i][j]=   True
            s = last_s+1
            self.areaMatrix[i][j] = s
            p = self.getProbability(s)
            sample = random.uniform(0,1)
            
            if(sample>p):
                return None
            # check if we can go in the four directions and act accordingly
            # i will be columns and j will be rows
            if (j+1)<self.latLength and not ((((i,j),(i,j+1)) in edges) or (((i,j+1),(i,j)) in edges)):
                edges.add(((i,j+1),(i,j)))
                edges.add(((i,j),(i,j+1)))
                dfs((i,j+1), visited, edges,s)
            if (i+1)<self.latLength and not ((((i,j),(i+1,j)) in edges) or (((i+1,j),(i,j)) in edges)):
                edges.add(((i+1,j),(i,j)))
                edges.add(((i,j),(i+1,j)))
                dfs((i+1,j), visited, edges,s)
            if (j-1)>self.latLength and not ((((i,j),(i,j-1)) in edges) or (((i,j-1),(i,j)) in edges)):
                edges.add(((i,j),(i,j-1)))
                edges.add(((i,j-1),(i,j)))
                dfs((i,j-1), visited, edges,s)
            if (i-1)>self.latLength and not ((((i,j),(i-1,j)) in edges) or (((i-1,j),(i,j)) in edges)):
                edges.add(((i-1,j),(i,j)))
                edges.add(((i,j),(i-1,j)))
                dfs((i-1,j), visited, edges,s)
            return None
        # the edges that are already existing 
        edges = set()
        visited = [[False for i in range(self.latLength)] for j in range(self.latLength)]
        visited[outlet[0]][outlet[1]] = True
        
        self.areaMatrix[outlet[0]][outlet[1]] = 1
        dfs((outlet[0],outlet[1]),visited,edges,0)
        #print(np.matrix(visited))
        print(edges)
    def calculateFlow(self):
        pass
    
    def plotPDF(self):
        # evaluate PDF
        x = np.linspace(0,50,100)
        pdf = [self.areaPDF.pdf(tmp_x) for tmp_x in x]
        #pdf = self.areaPDF.pdf(x)
        # plot
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, pdf, '--r')
        plt.title("Probability Density Function")
        plt.show()

    def plot(self):
        pass

if __name__=="__main__":
   
   riv = River(1.47,latLength=10)
   riv.populateLatMatix()


