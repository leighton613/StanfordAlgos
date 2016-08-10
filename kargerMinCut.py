
# coding: utf-8
"""
GOAL: randomized contraction algorithm for the min cut problem

FILE:
- adjacency list representation of a simple undirected graph
- The first column in the file represents the vertex label, 
 and other entries tells all the vertices that the vertex is adjacent to. 

"""
# In[1]:

import random
class Graph(object):
    class Vertex(object):
        __slots__ = '_id', '_adjacent'
        def __init__(self, id, adj=None):
            self._id = id
            self._adjacent = adj
        def _num_edges(self):
            return len(self._adjacent)
        def __str__(self):
            return "%r: id=%d" %(self.__class__, self._id)
        def __repr__(self):
            return self.__str__()
        
    def __init__(self, filename):
        self._vertices = {}                         # id to vertices
        self._n = 0
        self._m = 0
        
        # construct from file
        fh = open(filename)
        for line in fh:
            nums = [int(i) for i in line.strip().split()]
            adj = list(set(nums[1:]))
            vertex = self.Vertex(id=nums[0], adj=adj)
            
            self._vertices[nums[0]] = vertex
            self._n += 1
            self._m += (len(adj))
        assert(self._n == len(self._vertices))
        assert(self._m % 2 == 0)
        self._m /= 2                                # edges counted twice
        # print self.__str__()
    
    def __str__(self):
        return "%r: n=%d, m=%d" %(self.__class__, self._n, self._m)
    
    def __repr__(self):
        return "%r: n=%d, m=%d" %(self.__class__, self._n, self._m)
    
    def show(self):
        print self.__str__()
        for id, v in self._vertices.items():
            print "id=%d" %(id), "with adj", v._adjacent
        
    def select_edge(self):
        """ randomly seletct an edge and return two endpoints """
        num = random.randint(1, self._m)
        # print num
        
        v_exist = self._vertices.values()           # list of Vertex
        idx = 0
        temp_n = v_exist[idx]._num_edges()
        while num > temp_n:
            if idx >= len(v_exist)-1:
                raise ValueError("idx exceed self._vertices index range, i.e. num exceed m")
            num -= temp_n
            idx += 1
            temp_n = v_exist[idx]._num_edges()
        v1 = v_exist[idx]
        id2 = v1._adjacent[num-1]
        v2 = self._vertices[id2]
        # print "Selected id =", v1._id, "and id =", v2._id
        return [v1, v2]
    
    def edge_contraction(self, v1, v2):
        """ 
        Contract to the lower id one 
        1. delete higher one in self._adj AND add original
        2. delete adj[higher] in lower
        3. update higher -> lower in other vertices adj
        4. decrease self._n self._m
        """
        if v1._id < v2._id:
            v = v1
            v_del = v2
        else:
            v = v2
            v_del = v1
            
        # 1. delete higher one
        del self._vertices[v_del._id]
        # 2. delete adj[higher] in lower
        v._adjacent.remove(v_del._id)
        v_del._adjacent.remove(v._id)
        v._adjacent += (v_del._adjacent)
        # 3. update higher -> lower in other vertices adj
        self._m = 0
        for vertex in self._vertices.values():
            vertex._adjacent = [v._id if id==v_del._id else id for id in vertex._adjacent]
            vertex._adjacent = [id for id in vertex._adjacent if id!=vertex._id] # remove selfloop
            self._m += vertex._num_edges()
        # 4. decrease self._n self._m
        self._n -= 1
        assert(len(self._vertices) == self._n)
        assert(self._m % 2 == 0)
        self._m /= 2
        
        v_del._id = 0
        v_del._adjacent = []
    
    def min_cut(self):
        for i in range(self._n-2):
            [v1, v2] = self.select_edge()
            self.edge_contraction(v1,v2)
        return self._m


def Solution(filename):
    min_num = None
    for i in range(1000):
        G = Graph(filename)
        num = G.min_cut()
        if min_num == None or num < min_num:
            min_num = num
    return min_num




if __name__ == "__main__":
    print Solution("kargerMinCut.txt")



