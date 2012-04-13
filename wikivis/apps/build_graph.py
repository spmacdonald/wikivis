from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from wikivis.graph import WikiGraph

MAX_NODES = 9256791


def main():

    print 'Building graph...'
    g = WikiGraph(MAX_NODES)
    with open('datasets/wikipedia.abc', 'r') as fh:
        for i, line in enumerate(fh):
            u, v = line.split()
            g.insert_edge(int(u), int(v))

    print 'Building name dict...'
    names = {}
    with open('datasets/names.map', 'r') as fh:
        for line in fh:
            k, v = line.split()
            names[int(k)] = v


    print 'Starting JSON RPC Server...'
    server = SimpleJSONRPCServer(('localhost', 8080))
    server.register_function(g.successors, 'successors')
    server.register_function(g.predecessors, 'predecessors')
    server.register_function(names.get, 'name')
    server.serve_forever()


if __name__ == '__main__':
    main()
