from collections import defaultdict
from itertools import zip_longest
import networkx as nx
import matplotlib.pyplot as plt

class Vertex:
    def __init__ (self, node):
        self.id= node
        self.adjacent = {}

    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] =weight
    def getConnections(self):
        return self.adjacent.keys()
    def getVertexlD(self):
        return self.id
    def getWeight(self, neighbor):
        return self.adjacent[neighbor]


    def __str__ (self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
                                                  
class Graph:
    def __init__ (self):
        self. vertDictionary = {}
        self.numVertices = 0
        self.vertexPath=defaultdict(list)
        self.allPaths=[]
    
    def __iter__ (self):
        return iter(self.vertDictionary.values())
    
    
    
    def addVertex(self, node):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(node)
        self.vertDictionary[node] = newVertex
        return newVertex
    
    def getVertex(self, n):
        if n in self.vertDictionary:
            return self.vertDictionary[n]
        else:
            return None
        
    def addEdge(self, frm, to, cost= 0):
        if frm not in self.vertDictionary:
            self.addVertex(frm)
        if to not in self.vertDictionary:
            self.addVertex(to)
        self.vertDictionary[frm].addNeighbor(self.vertDictionary[to], cost)
        self.vertexPath[frm].append(to)

        #For undirected graph add this two rows
        # self.vertDictionary[to].addNcighbor(self. vertDictionary[frm], cost)
        # self.vertexPath[to].append(frm)

    def getEdges(self):
        edges= []
        for v in G:
            for w in v.getConnections():
                vid = v.getVertexlD()
                wid = w.getVertexlD()
                edges.append((vid, wid, v.getWeight(w)))
        return edges
    
    def getVertices(self):
        return self.vertDictionary.keys()
    
    def getAllTracksUtil(self, frm, to, visited, path):

        visited[frm]= True 
        path.append(frm)

        if frm == to:  
            self.allPaths.append(tuple(path))
        else:
            for i in self.vertexPath[frm]: 
                if visited[i]== False:
                    self.getAllTracksUtil(i, to, visited, path)
                    
        path.pop()
        visited[frm]= False


    def getAllTracks(self, frm, to):
        visited={n:False for n in self.getVertices()}
        path = []
        self.getAllTracksUtil(frm, to, visited, path)
        
    def calculateCost(self):
        calc=defaultdict(int)
        for count,track in enumerate(self.allPaths):
            number=0
            for x,y in zip_longest(track,track[1:]):
                if y==None:
                    break
                number += self.getVertex(x).getWeight(self.getVertex(y))
            calc[count]=number 
            
        return calc       
                
                
    def Search_Algorithm(self,frm,to):
        self.allPaths=[]
        self.getAllTracks(frm,to)
        costs=self.calculateCost()
        
        if costs:
            correctposition=min(costs,key=lambda n:costs[n])
            correctPath=self.allPaths[correctposition]
            print(f'All possible paths from node {frm} to node {to} :')
            for track,cost in zip(self.allPaths,costs.values()):
                print('     ',str(track),' -->>> with cost : ', cost)
            
            print('\n','********** Search Algorithm **********')
            print('The best path has the lowest cost : ') 
            print('     ',str(correctPath),' -->>> with cost : ', costs[correctposition])   
        else:
            print(f'There are not any path from node {frm} to node {to} ')
            return ('No Path',frm,to)
                
        return correctPath
    
    def colorMap(self,track,graph):
        color_map = []
        if track[0] == 'No Path':
            for node in graph.nodes():
                if node in track:
                    color_map.append('red')
                else: 
                    color_map.append('blue')
        else:
            for node in graph.nodes():
                if node in track:
                    color_map.append('green')
                else: 
                    color_map.append('blue')                    
        return color_map
                        
    

if __name__ == '__main__':
    G =Graph()
    G.addEdge('s', 'a', 2)
    G.addEdge('s', 'd', 10)
    G.addEdge('a', 'd', 4)
    G.addEdge('a', 'b', 4)
    G.addEdge('a', 'g', 6)
    G.addEdge('b', 'g', 8)
    G.addEdge('d', 'e', 14)
    G.addEdge('g', 'e', 10)
    G.addEdge('b', 'f', 7)
    G.addEdge('f', 's', 2)
    # G.addEdge('h', 'i', 6)

    


    path=G.Search_Algorithm('s','e') 
      
    graphDraw=nx.DiGraph()
    graphDraw.add_weighted_edges_from(G.getEdges())
    
    plt.figure(figsize=(10,5))
    ax = plt.gca()
    if path[0]=='No Path':
        ax.set_title(f'Search algorithm path from node {repr(path[1])} to node {repr(path[2])} :\n {str(path[0])}')
    else:
        ax.set_title(f'Search algorithm path from node {repr(path[0])} to node {repr(path[-1])} :\n {str(path)}')
            
    nx.draw(graphDraw, with_labels=True,pos=nx.circular_layout(graphDraw),
        node_size=2400,node_color=G.colorMap(path,graphDraw))
    nx.draw_networkx_edges(graphDraw, pos=nx.circular_layout(graphDraw),
                       arrowsize=35)
    
    plt.show()