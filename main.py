import networkx as nx

import annealing
import graph

def main():
    n = 24
    k = 4

    anneal = annealing.Annealing(graph.init_pop(n, k, 100))
    ret_ind = anneal.solve(True)

    print("Optimized")
    print('Diameter: {:.3f}'.format(nx.diameter(ret_ind.G)))
    print('ASPL: {:.3f}'.format(ret_ind.aspl))
    with open('regular-graph-o{}-d{}.gml'.format(n, k), 'wb') as f:
        nx.write_gml(ret_ind.G, f)

if __name__ == "__main__":
    main()