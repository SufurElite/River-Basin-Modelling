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
    def __init__(self,fractalDim:float, latLength: int = 100, upstream:bool = False, outlet:tuple[int, int] = (0,0)):
        self.upstream = upstream
        self.outlet = outlet      
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
        # initially represent the graph as a dictionary of nodes
        # to edges
        self.dict_graph = {}
        self.G = nx.Graph()
        # correspondence of node to location
        self.nodeLocs = {}

        self.populateLatMatix()
        self.createGraph()
        
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
            # return np.exp(-x)**2
            # return 1-0.8*((np.exp(-0.005*x)-1)/(np.exp(-5.475)-1))
            return np.sin(x)/x
        
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
    
    def createGraph(self):
        """
            Once populate matrix has been run, we 
            create an NX graph to visualise
        """
        
        nodes = list(self.dict_graph.keys())
        node_to_name = {}
        for i in range(len(nodes)):
            node_to_name[nodes[i]] = chr(65+i)
        
        for node in self.dict_graph:
            nodeName = node_to_name[node] + " " + str(self.areaMatrix[node[0]][node[1]])
            if self.outlet == (node[0], node[1]):
                nodeName = "[Outlet] " + nodeName
            
            self.nodeLocs[nodeName] = (node[0],self.latLength-node[1])

            for edge in self.dict_graph[node]:
                otherNode = node_to_name[(edge[0],edge[1])] + " " + str(self.areaMatrix[edge[0]][edge[1]])
                self.G.add_edge(nodeName,otherNode,weight=edge[2])
        
    def populateLatMatix(self):
        def dfs(coords, visited, edges,last_s):
            i, j = coords[0], coords[1]
            if not visited[i][j]:
                visited[i][j] = True
                self.dict_graph[(i,j)] = []
            
            self.latticeMatrix[i][j] = 1

            s = last_s+1
            # not sure if it should be the total merged 
            # or just the one time and then should the river
            # add the values on to the final area
            self.areaMatrix[i][j] = s
            
            p = self.getProbability(s)
            sample = random.uniform(0,1)
            
            if(sample>p):
                return None
            # check if we can go in the three directions and act accordingly
            if (j+1)<self.latLength and not ((((i,j),(i,j+1)) in edges) or (((i,j+1),(i,j)) in edges)):
                edges.add(((i,j),(i,j+1)))
                edges.add(((i,j+1),(i,j)))
                self.dict_graph[(i,j)].append((i,j+1,p))

                dfs((i,j+1), visited, edges,s)
            if (i+1)<self.latLength and not ((((i,j),(i+1,j)) in edges) or (((i+1,j),(i,j)) in edges)):
                edges.add(((i+1,j),(i,j)))
                edges.add(((i,j),(i+1,j)))
                self.dict_graph[(i,j)].append((i+1,j,p))

                dfs((i+1,j), visited, edges,s)
            if (j-1)>0 and not ((((i,j),(i,j-1)) in edges) or (((i,j-1),(i,j)) in edges)):
                edges.add(((i,j),(i,j-1)))
                edges.add(((i,j-1),(i,j)))
                self.dict_graph[(i,j)].append((i,j-1,p))
                
                dfs((i,j-1), visited, edges,s)
            """if (i-1)>0 and not ((((i,j),(i-1,j)) in edges) or (((i-1,j),(i,j)) in edges)):
                edges.add(((i-1,j),(i,j)))
                edges.add(((i,j),(i-1,j)))
                self.dict_graph[(i,j)].append((i-1,j,p))
                dfs((i-1,j), visited, edges,s)"""
            return None
        # the edges that are already existing 
        edges = set()
        visited = [[False for i in range(self.latLength)] for j in range(self.latLength)]
        visited[self.outlet[0]][self.outlet[1]] = True
        self.latticeMatrix[self.outlet[0]][self.outlet[1]] = 1
        self.areaMatrix[self.outlet[0]][self.outlet[1]] = 0
        self.dict_graph[(self.outlet[0],self.outlet[1])] = []

        dfs((self.outlet[0],self.outlet[1]),visited,edges,0)

    def calculateFlow(self):
        pass
    
    def plotPDF(self):
        """
            Plot the PDF as a function of area
        """
        # area of 0 to 50 by increments of 2 (100/50=2)
        x = np.linspace(0,50,100)
        pdf = [self.areaPDF.pdf(tmp_x) for tmp_x in x]
        
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, pdf, '--r')
        plt.title("Probability Density Function")
        plt.xlabel("Area")
        plt.ylabel("Probability (%)")
        plt.show()

    def pprint(self):
        print("="*20)
        print("Area Matrix: ")
        print(self.areaMatrix)
        print("="*20)
        print("Lattice Matrix: ")
        print(self.latticeMatrix)
    
    def plotGraph(self, save:bool = False):
        plt.rcParams["figure.figsize"] = (10,10)
        sumWeights = 0
        totalWeights = 0
        uniqueWeights = set()
        
        for node in self.dict_graph:
            totalWeights+=len(self.dict_graph[node])    
            for edge in self.dict_graph[node]:
                sumWeights+=edge[2]
                uniqueWeights.add(edge[2])

        pos = nx.spring_layout(self.G,pos=self.nodeLocs,fixed=self.nodeLocs.keys())
        # nodes
        nx.draw_networkx_nodes(self.G,pos,node_size=800)
        nx.draw_networkx_labels(self.G,pos,font_size=18)
        # edges
        for weight in uniqueWeights:
            weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in self.G.edges(data=True) if edge_attr['weight']==weight]
            nx.draw_networkx_edges(self.G,pos,edgelist=weighted_edges,width=weight*4*totalWeights/sumWeights, arrows=True, edge_color="cyan")
        
        plt.axis('off')
        plt.title(f"Saved River Fractal Dimension: {(self.fractalDim)}")
        if save:
            plt.savefig("plots/river_weighted_graph.png") # save as png
        plt.show() # display

if __name__=="__main__":
   
  # riv = River(1.47,latLength=10, outlet=(2,2))
   riv = River(1.47,latLength=10)
   riv.pprint()
   riv.plotGraph()
   