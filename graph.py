import networkx
import networkx as nx

class Graph:
    def __init__(self, G, aspl=None):
        self.G = G
        self.aspl = aspl
        self.count = 0

    def copy(self):
        return Graph(self.G.copy(as_view=False), self.aspl)

def calc_aspl(G):
    try:
        score = nx.average_shortest_path_length(G)
    except networkx.NetworkXError:
        score = float('inf')
    return score


def init_pop(n_node, n_degree, n_ind):
    pop = []
    global count
    for i in range(n_ind):
        G = nx.random_regular_graph(d=n_degree, n=n_node)
        ind = Graph(G)
        pop.append(ind)
    print(count)

    if count == 1:
        print("Random")
        print('Diameter: {:.3f}'.format(nx.diameter(ind.G)))
        print('ASPL: {:.3f}'.format(calc_aspl(ind.G)))

    count = 1

    return pop
