import copy

import networkx as nx
import sys
import numpy as np
from webweb import Web


def DFS(g,v,visited): #DFS to count nodes
    visited.append(v)
    for edge in g.edges(v):
        if edge[1] not in visited:
                DFS(g,edge[1],visited)
def get_neighbors(g,id):
    neighbors = []
    for edge in g.edges(id):
        neighbors.append(edge[1])
    return neighbors
def num_verts(g):
    visited = []
    nodes = list(g.nodes())
    DFS(g,nodes[0],visited)
    visited.sort()
    return len(visited)
def calcdegree(g, id):
    sum = 0
    for edge in g.edges(id):
        sum+=1
    return sum
def clustering(g,id):
    c = 0
    neighbors = get_neighbors(g,id)
    counted = []
    for n in neighbors:
        for edge in g.edges(n):
            if edge[0] in neighbors and edge[1] in neighbors:
                edge = sorted(edge)
                if edge not in counted:
                    c+=1
                    counted.append(edge)
    val = copy.deepcopy(calcdegree(g, id))
    bottom = ((val-1)*(val))
    if bottom == 0:
        coeff = 0
    else:
        coeff = 2*(float(c))/bottom
    return coeff

def betweenness(g,id):
    sum = 0
    top = 0
    bot = 0
    for i in g:
        for j in g:
            if i != j and i != id:
                paths = nx.all_shortest_paths(g, source=i, target=j)
                for p in paths:
                    bot+=1
                    if id in p:
                        top +=1
            if bot != 0:
                sum+=(top/bot)
        print(i)
    return sum

def adjacency(g):
    #returns a sorted matrix with newly mapped vals
    vals = []
    for i in range(len(g.nodes())):
        vals.append(i)
    labels = dict(zip(sorted(g.nodes()), vals))
    newg = nx.relabel_nodes(g,mapping=labels)
    m = []
    n = num_verts(g)
    for i in range(n):
        m.append([0 for i in range(n)])
    for edge in newg.edges():
        m[edge[0]][edge[1]] = 1
        m[edge[1]][edge[0]] = 1

    return m, labels
def prestige(m):
    vector = np.ones(len(m))
    lastv = np.ones(len(m))
    i = 0
    while i < 1000:
        lastv = vector
        vector = np.dot(m,lastv)
        i+=1
        print(vector)
    return vector
def main():
    sys.setrecursionlimit(10000)
    f = open("oregon1_010331.txt", 'r')
    g = nx.Graph()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    for line in f:
        arr = line.split("\t")
        arr[1] = arr[1].strip("\n")
        g.add_edge(int(arr[0].strip()),int(arr[1].strip()))
    edge_list = []
    for edge in g.edges:
        edge_list.append([edge[0],edge[1]])
    degrees = []
    edge_list = edge_list[-4000:]
    web = Web(edge_list)
    web.show()
    for node in g.nodes:
        degrees.append(calcdegree(g,node))
    x = dict(zip(g.nodes,degrees))
    x = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    print("Top 10 nodes by highest degree in reverse order, nodes come first")
    print(list(x.items())[-10:])
    x = {k: v for k, v in sorted((nx.betweenness_centrality(g, 100).items()), key=lambda item: item[1])}
    print("Top 10 nodes by betweeness in reverse order, nodes come first")
    print(list(x.items())[-10:])
    print("Top 10 nodes by clustering in reverse order, nodes come first")
    cls = []
    for node in g.nodes:
        cls.append(clustering(g, node))
    x = dict(zip(g.nodes, cls))
    x = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    print(list(x.items())[-10:])
    print("Top 10 nodes by prestige in reverse order, nodes come first")
    x = {k: v for k, v in sorted(nx.eigenvector_centrality(g).items(), key=lambda item: item[1])}
    print(list(x.items())[-10:])
    print("Top 10 nodes by pagerank in reverse order, nodes come first")
    x = {k: v for k, v in sorted(nx.pagerank(g).items(), key=lambda item: item[1])}
    print(list(x.items())[-10:])

main()