#include <iostream>
#include <vector>

namespace WikiGraph {

template <typename T>
class Graph
{
public:

    Graph(size_t n) : _pred(n), _succ(n) { };
    ~Graph() {};

    size_t size() { return _pred.size(); }
    void insert_edge(const T&, const T&);
    const std::vector<T>& predecessors(const T& n) const { return _pred[n]; }
    const std::vector<T>& successors(const T& n) const { return _succ[n]; }

private:

    std::vector<std::vector<T> > _pred;
    std::vector<std::vector<T> > _succ;

};


template <typename T>
void Graph<T>::insert_edge(const T& u, const T&v)
{
    _succ[u].push_back(v);
    _pred[v].push_back(u);
}


} // namespace
