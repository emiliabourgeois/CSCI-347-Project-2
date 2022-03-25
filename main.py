import copy

import networkx as nx
import numpy
import sys

from matplotlib import pyplot as plt


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
    coeff = 2*(float(c))/((val-1)*(val))
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

    return m
def prestige(m):
    return False
def main():
    sys.setrecursionlimit(10000)
    f = open("oregon1.txt", 'r')
    g = nx.Graph()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    for line in f:
        arr = line.split("\t")
        arr[1] = arr[1].strip("\n")
        g.add_edge(int(arr[0].strip()),int(arr[1].strip()))
    ##print(num_verts(g))
   # print(g.degree[1])
    #print(calcdegree(g, 1))
   # print(nx.clustering(g,1))
  #  print(clustering(g,1))
    print(nx.betweenness_centrality(g,10))
    #print(betweenness(g,10000))
    nx.draw_planar(g)

    plt.show()
    #adj = adjacency(g)
    #print(nx.eigenvector_centrality(g))
main()