
# coding: utf-8

"""
GOAL: computing strongly connected components (SCCs)
FILE:
- The file contains the edges of a directed graph. Vertices are labeled as positive integers from 1.
- Every row indicates an edge (tail -> head)
"""

class Graph(object):
    class _Vertex(object):
        __slots__ = '_id', '_in_edges', '_out_edges'
        def __init__(self, id, in_edges=None, out_edges=None):
            self._id = id
            if in_edges == None:  self._in_edges = []
            else: self._in_edges= in_edges
            if out_edges == None: self._out_edges = []
            else: self._out_edges = out_edges
        def __str__(self):
            return "Node %d" %self._id
        def __repr__(self):
            return self.__str__()
        
    class _Edge(object):
        __slots__ = '_id', '_tail', '_head'
        def __init__(self, id, tail, head):
            """ tail & head are Vertex id"""
            self._id = id
            self._tail = tail
            self._head = head
        def __str__(self):
            return "Edge %d: %r -> %r" %(self._id, self._tail, self._head)
        def __repr__(self):
            return self.__str__()
        
    def __init__(self, filename):
        fh = open(filename)
        self._edges = []
        self._vertices = []
        self._m = None                   # number of edges
        self._n = None                   # number of vertices
        
        # edges
        self._m = 0
        for line in fh:
            self._m += 1
            nums = [int(i) for i in line.strip().split()]
            edge = self._Edge(id=self._m, tail=nums[0], head=nums[1])
            self._edges.append(edge)
            if self._n == None or max(nums) > self._n:
                self._n = max(nums)
        
        # vertices
        for idx in range(self._n):
            v = self._Vertex(idx+1)
            self._vertices.append(v)
        # self._check_edges()
        
        for e in self._edges:
            self._vertices[e._tail-1]._out_edges.append(e._id)
            self._vertices[e._head-1]._in_edges.append(e._id)
            # self._check_edges()
        
        # error check
        assert(len(self._edges)==self._m and len(self._vertices)==self._n)
        cnt = 0
        for v in self._vertices:
            cnt += (len(v._out_edges) + len(v._in_edges))
        assert(cnt == 2*self._m)
        print "Loaded:", self.__str__()
        
        # prepare for scc
        self.fns_time = [None for i in range(self._n)]
        self.leaders = [id for id in range(1, self._n+1)]
        self.explore_map = [False for i in range(self._n)]
        self.t = 0
        self.s = None
    
    def __str__(self):
        return "Graph: %d edges, %d vertices." %(self._m, self._n)
    
    def __repr__(self):
        return __str__()
    
    def show(self):
        print self.__str__()
        for e in self._edges:
            print e.__str__()
    
    def _check_edges(self):
        for v in self._vertices:
            print v, v._out_edges, v._in_edges
    
    # the whole scc function
    def scc(self):
        self.DFS_loop(reverse=True)
        self.DFS_loop(reverse=False)
        
        # computer leaders
        cnt = {}
        for i in range(self._n):
            cnt[self.leaders[i]] = cnt.get(self.leaders[i],0) + 1
        temp = cnt.values()
        temp.sort(reverse=True)
        if len(cnt) > 5:
            print temp[0:5]
        else:
            print temp
        
    def DFS(self, node_id, reverse):
            """ 
            node_id: id of node
            explore_map: list[bool]
            """
            node = self._vertices[node_id-1]
            self.explore_map[node_id-1] = True
            if reverse == True:              # first pass
                for e_id in node._in_edges:
                    in_id = self._edges[e_id-1]._tail
                    if self.explore_map[in_id-1] == False:
                        self.DFS(in_id, reverse)
                self.t += 1
                self.fns_time[node_id-1] = self.t
            else:                            # second pass
                self.leaders[node_id-1] = self.s
                for e_id in node._out_edges:
                    out_id = self._edges[e_id-1]._head
                    if self.explore_map[out_id-1] == False:
                        self.DFS(out_id, reverse)
                        
    def DFS_loop(self, reverse=False):
        self.explore_map = [False for i in range(self._n)]
        if reverse == True:                   # first pass
            self.t = 0                        # finishing time
            self.fns_time = [None for i in range(self._n)]
        else:
            self.s = None                     # leaders for second pass
            self.leaders = [id for id in range(1, self._n+1)]
            # print "finishing time", self.fns_time
            idx_order = [i[0] for i in sorted(enumerate(self.fns_time), 
                                            key=lambda x: x[1])] # ascending

        for idx in range(self._n-1, -1, -1):
            if reverse == False:              # second pass
                idx = idx_order[idx]
            if self.explore_map[idx] == False:
                self.s = idx+1
                self.DFS(idx+1,reverse=reverse)



import sys
sys.setrecursionlimit(80000)
def Solution(filename):
    G = Graph(filename)
    G.scc()



if __name__ == "__main__":
    Solution("SCC.txt")
