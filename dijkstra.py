
# coding: utf-8

"""
GOAL: 
- Dijkstra's shortest-path algorithm;
FILE:
- Each row consists of the node tuples that are adjacent to that particular vertex along with the **length** of that edge. 
- For example, the 6th row has 6 as the first entry indicating that this row corresponds to the vertex labeled 6. 
  The next entry of this row "141,8200" indicates that there is an edge between vertex 6 and vertex 141 that has length 8200.
"""


import numpy as np



class Graph(object):
    '''undirected, weighted Graph'''
    class _Vertex(object):
        __slots__ = '_id', '_edges'
        def __init__(self, id):
            self._id = id
            self._edges = []
        
        def __str__(self):
            return "Vertex %d with adj. edges %r" %(self._id, self._edges)
        
        def __repr__(self):
            return self.__str__()
    
    
    def __init__(self, filename):
        self._vertices = []
        self._n = 0
        self._m = 0
        
        fh = open(filename)
        for line in fh:
            self._n += 1
            eles = line.strip().split()
            assert(self._n == int(eles.pop(0)))
            v = self._Vertex(id=self._n)
            for e in eles:
                nums = [int(i) for i in e.split(',')]
                v._edges.append((nums[0], nums[1]))
                self._m += 1
            self._vertices.append(v)
        
        assert(self._n == len(self._vertices))
        assert(self._m % 2 == 0)    # counted twice
        self._m /= 2
        
        print self.__str__()
        
        # prepare for dijkstra
        self.A = [np.inf for i in range(self._n)]
        
    def __str__(self):
        return 'Graph with %d vertices and %d edges.' %(self._n, self._m)
        
    def __repr__(self):
        return self.__str__()
    
    def dijkstra(self, s=1):
        s = s
        Expd = [s]
        Unexpd = [i for i in range(1,self._n+1)]
        Unexpd.remove(s)
        
        self.A[s-1] = 0
        for iteration in range(1,self._n):
            minPath, v_inSet, v_notinSet = self.dijkstra_greedy_criterion(Expd)
            # print 'iter', iteration, v_inSet, v_notinSet
            Expd.append(v_notinSet)
            Unexpd.remove(v_notinSet)
            self.A[v_notinSet-1] = minPath
            
        test = [7,37,59,82,99,115,133,165,188,197]
        print [self.A[i-1] for i in test]
        
    def dijkstra_greedy_criterion(self, Set):
        minPath = None
        v_notinSet = None
        v_inSet = None
        
        for v_id in Set:
            for e in self._vertices[v_id-1]._edges:
                # e: (v2_id, cost)
                if e[0] not in Set: # crossing edge
                    tempPath = self.A[v_id-1] + e[-1]
                    if minPath == None or tempPath < minPath:
                        minPath = tempPath
                        v_notinSet = e[0]
                        v_inSet = v_id
        return minPath, v_inSet, v_notinSet



def Solution():
    G = Graph('dijkstraData.txt')
    G.dijkstra()



if __name__ == "__main__":
    Solution()

