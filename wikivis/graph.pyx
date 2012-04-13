from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.vector cimport vector


cdef extern from "graph.hpp" namespace "WikiGraph":
    cdef cppclass Graph[T]:
        Graph(size_t)
        size_t size()
        void insert_edge(T&, T&)
        vector[T]& successors(T&)
        vector[T]& predecessors(T&)


ctypedef size_t node_type

cdef class WikiGraph:

    cdef Graph[node_type] *thisptr

    def __cinit__(self, size_t max_nodes):
        self.thisptr = new Graph[node_type](max_nodes)

    def __dealloc__(self):
        del self.thisptr

    def __len__(self):
        return self.thisptr.size()

    def insert_edge(self, node_type u, node_type v):
        self.thisptr.insert_edge(u, v)

    def successors(self, node_type n):
        cdef vector[node_type] succ = self.thisptr.successors(n)
        cdef vector[node_type].iterator it = succ.begin()

        result = []
        while it != succ.end():
            result.append(deref(it))
            inc(it)

        return result

    def predecessors(self, node_type n):
        cdef vector[node_type] pred = self.thisptr.predecessors(n)
        cdef vector[node_type].iterator it = pred.begin()

        result = []
        while it != pred.end():
            result.append(deref(it))
            inc(it)

        return result



