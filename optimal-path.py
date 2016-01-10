# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
# In this problem, graphs nodes are the buildings and the edges are the total
# and outdoor distances,
# 



def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    dg=WeightedDigraph()
    print "Loading map from file..."
    infile=open(mapFilename, 'r')
    for line in infile:
        data=line.strip()
        data=data.split()
        node0=Node(data[0])
        node1=Node(data[1])
        if not dg.hasNode(node0):
            dg.addNode(node0)
        if not dg.hasNode(node1):
            dg.addNode(node1)
        edge=WeightedEdge(node0,node1,float(data[2]),float(data[3]))
        dg.addEdge(edge)
        
    infile.closed
    return dg

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result



def distanceTotal(graph,path=[]):
    totalDistance=0.0
    if not path==None and len(path) >= 2:
        for j in range(len(path)-1):
            startNode=filter(lambda x: x.getName()==path[j], graph.nodes)[0]
            edge_info=filter(lambda x: x[0].getName()==path[j+1], graph.edges[startNode])[0]
            #print edge_info
            totalDistance+=float(edge_info[1][0])
    return totalDistance


def distanceOutdoor(graph,path=[]):
    outdoorDistance=0.0
    if  not path==None and len(path) >= 2:
        for j in range(len(path)-1):
            startNode=filter(lambda x: x.getName()==path[j], graph.nodes)[0]
            edge_info=filter(lambda x: x[0].getName()==path[j+1], graph.edges[startNode])[0]
            #print edge_info
            outdoorDistance+=float(edge_info[1][1])
    return outdoorDistance
        




def DFSAll(graph, start, end, path, paths = []):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph 
    #print start
    path=path+[start]
    startNode=filter(lambda x: x.getName()==start, graph.nodes)[0]

    if start==end:
        paths.append(path)
        return paths
    
    for node in graph.childrenOf(startNode):
        if node.getName() not in path: #avoid cycles
                paths = DFSAll(graph,node.getName(),end, path, paths)         
    return paths                              


def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    paths=DFSAll(digraph, start, end,path=[],paths=[])
    
    if paths==None:
        shortest=None
    else:
        paths=filter(lambda x: distanceOutdoor(digraph,x)<=maxDistOutdoors,paths)
        if not paths:
            shortest=None
        else:
            shortest=reduce(lambda x,y: x if distanceTotal(digraph,x) < distanceTotal(digraph,y) else y,paths)
            if distanceTotal(digraph,shortest) > maxTotalDist:
                shortest = None
            
    if shortest == None:
        raise ValueError()
    else:
        return shortest


def DFSShortest(graph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph

    startNode=filter(lambda x: x.getName()==start, graph.nodes)[0]

    path = path + [start]

    if start == end:
        return path
    for node in graph.childrenOf(startNode):
        if node.getName() not in path: #avoid cycles
            totalDistanceShortest=distanceTotal(graph,shortest)
            totalDistance=distanceTotal(graph,path+[node.getName()])
            outdoorDistance=distanceOutdoor(graph,path+[node.getName()])
            if shortest == None or totalDistance<=totalDistanceShortest and outdoorDistance<=maxDistOutdoors and totalDistance<=maxTotalDist:
                newPath = DFSShortest(graph,node.getName(),end, maxTotalDist, maxDistOutdoors, path,shortest)
                if newPath != None and distanceTotal(graph,newPath)  <= maxTotalDist and distanceOutdoor(graph,newPath)  <= maxDistOutdoors:
                    shortest = newPath

    return shortest


#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    shortest=DFSShortest(digraph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = None)
    if shortest == None:
        raise ValueError()
    else:
        return shortest


# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
# if __name__ == '__main__':
#     Test cases
#     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges


#     LARGE_DIST = 1000000

#     Test case 1
#     print "---------------"
#     print "Test case 1:"
#     print "Find the shortest-path from Building 32 to 56"
#     expectedPath1 = ['32', '56']
#     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath1
#     print "Brute-force: ", brutePath1
#     print "DFS: ", dfsPath1
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
#     print "---------------"
#     print "Test case 2:"
#     print "Find the shortest-path from Building 32 to 56 without going outdoors"
#     expectedPath2 = ['32', '36', '26', '16', '56']
#     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
#     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
#     print "Expected: ", expectedPath2
#     print "Brute-force: ", brutePath2
#     print "DFS: ", dfsPath2
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
#     print "---------------"
#     print "Test case 3:"
#     print "Find the shortest-path from Building 2 to 9"
#     expectedPath3 = ['2', '3', '7', '9']
#     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath3
#     print "Brute-force: ", brutePath3
#     print "DFS: ", dfsPath3
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
#     print "---------------"
#     print "Test case 4:"
#     print "Find the shortest-path from Building 2 to 9 without going outdoors"
#     expectedPath4 = ['2', '4', '10', '13', '9']
#     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
#     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
#     print "Expected: ", expectedPath4
#     print "Brute-force: ", brutePath4
#     print "DFS: ", dfsPath4
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
#     print "---------------"
#     print "Test case 5:"
#     print "Find the shortest-path from Building 1 to 32"
#     expectedPath5 = ['1', '4', '12', '32']
#     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
#     print "Expected: ", expectedPath5
#     print "Brute-force: ", brutePath5
#     print "DFS: ", dfsPath5
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
#     print "---------------"
#     print "Test case 6:"
#     print "Find the shortest-path from Building 1 to 32 without going outdoors"
#     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
#     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
#     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
#     print "Expected: ", expectedPath6
#     print "Brute-force: ", brutePath6
#     print "DFS: ", dfsPath6
#     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
#     print "---------------"
#     print "Test case 7:"
#     print "Find the shortest-path from Building 8 to 50 without going outdoors"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
#     print "---------------"
#     print "Test case 8:"
#     print "Find the shortest-path from Building 10 to 32 without walking"
#     print "more than 100 meters in total"
#     bruteRaisedErr = 'No'
#     dfsRaisedErr = 'No'
#     try:
#         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         bruteRaisedErr = 'Yes'
    
#     try:
#         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
#     except ValueError:
#         dfsRaisedErr = 'Yes'
    
#     print "Expected: No such path! Should throw a value error."
#     print "Did brute force search raise an error?", bruteRaisedErr
#     print "Did DFS search raise an error?", dfsRaisedErr


g = WeightedDigraph()
n1 = Node('1')
n2 = Node('2')
n3 = Node('3')
n4 = Node('4')
n5 = Node('5')
g.addNode(n1)
g.addNode(n2)
g.addNode(n3)
g.addNode(n4)
g.addNode(n5)
e1 = WeightedEdge(n1, n2, 10.0, 5.0)
e2 = WeightedEdge(n1, n4, 5.0, 1.0)
e3 = WeightedEdge(n2, n3, 8.0, 5.0)
e4 = WeightedEdge(n4, n3, 8.0, 5.0)
#e5 = WeightedEdge(n4, n3, 5.0, 1.0)
#e6 = WeightedEdge(n4, n5, 20.0, 1.0)
#print e3
g.addEdge(e1)
g.addEdge(e2)
g.addEdge(e3)
g.addEdge(e4)
#g.addEdge(e5)
#g.addEdge(e6)
print g
#print DFSAll(g, '1', '5',paths)
print bruteForceSearch(g, "1", "3", 18, 18)
print directedDFS(g, "1", "3", 18, 18)
#print paths
#print bruteForceSearch(g, "1", "5", 35, 8)
#print bruteForceSearch(g, "4", "5", 21, 11)
#print bruteForceSearch(g, "4", "5", 21, 1)
#print bruteForceSearch(g, "4", "5", 19, 1)
