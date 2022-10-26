import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
import math

from torch import is_tensor

neighbor_map = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

def load_occupancy_map():
	# Read image from disk using PIL
	occupancy_map_img = Image.open('/Users/anushsriramramesh/Library/CloudStorage/OneDrive-NortheasternUniversity/MR/MR-HW3/Utilities/occupancy_map.png')
	occupancy_grid = (np.asarray(occupancy_map_img) > 0).astype(int)
	return occupancy_grid

def rejectionSampler(occupancyGrid):
    sampleSetVertices = []
    for x in range(occupancyGrid.shape[0]):
        for y in range(occupancyGrid.shape[1]):
            sampleSetVertices.append((x,y))
    return sampleSetVertices[np.random.randint(0, len(sampleSetVertices))]

def Neighbours(graph, v):
    neighbors = []
    for x,y in neighbor_map:
        search_point = (v[0]+x,v[1]+y)
        neighbors.append(search_point)
    return neighbors

def reachabilityCheck(occupancyGrid, v1, v2):
    print("v1: ", v1)
    print("v2: ", v2)
    current = v1
    while current != v2:
        neighbors = Neighbours(occupancyGrid, current)
        current = min(neighbors, key=lambda x: math.dist(x, v2))
        if occupancyGrid[current] == 0:
            return False
        else:
            continue
    return True

class PRM():
    def __init__(self, N, dmax) -> None:
        super().__init__()
        self.graph = nx.Graph()
        self.vertices = []
        self.edges = []
        self.occupancy_grid = load_occupancy_map()
        self.NumberOfSamples = N
        self.maxDistance = dmax

    def build_graph(self):
        for i in range(self.NumberOfSamples):
            sampleVertex = rejectionSampler(self.occupancy_grid)
            self.addVertex(sampleVertex, i)
        #print("sampleV", sampleSetVertices)
    def addVertex(self, sampleVertex, itr):
        #print("sampleVertex", sampleVertex)
        self.graph.add_node(itr, pos=sampleVertex)
        # print("graph", self.graph.nodes[itr]['pos'])
        # print("graph", self.graph.nodes[itr]['pos'])
        for v in self.graph.nodes:
            print("v", v)
            if self.graph.nodes[v]['pos'] != sampleVertex:
                if (reachabilityCheck(self.occupancy_grid, sampleVertex, self.graph.nodes[v]['pos'])) and (math.dist(sampleVertex, self.graph.nodes[v]['pos']) <= self.maxDistance):
                    self.graph.add_edge(self.graph.nodes[v][0],itr, weight=math.dist(sampleVertex, self.graph.nodes[v]['pos']))
            else:
                return
        return None

if __name__ == "__main__":
    prm = PRM(2500, 75)
    prm.build_graph()
    nx.draw_networkx(prm.graph)
