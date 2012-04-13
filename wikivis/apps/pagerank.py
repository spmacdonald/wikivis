import networkx as nx
import jsonrpclib

server = jsonrpclib.Server('http://localhost:8080')

print server.predecessors(5)
print
print server.successors(5)

G = nx.DiGraph()

n = 1
for x in server.successors(n):
    G.add_edge(n, x)

for x in server.predecessors(n):
    G.add_edge(x, n)

pr = nx.pagerank(G)
print sorted(pr.items(), key=lambda x: x[1], reverse=True)

print server.name(561667)
