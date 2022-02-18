import math

import extended_networkx_tools as ext
import random

import networkx as nx


class Annealing:
    temperature = 10000

    current_graph = None
    adjacency_matrix = None
    row_length = None
    energy_cost = None
    max_energy_cost = None

    def __init__(self, g):
        self.current_graph = g
        self.adjacency_matrix = ext.Analytics.get_neighbour_matrix(g)
        self.row_length = len(self.current_graph.nodes())
        self.max_energy_cost = ext.Analytics.hypothetical_max_edge_cost(g)
        self.energy_cost = self.get_energy(g)

    def solve(self) -> object:

        if not nx.is_connected(self.current_graph):
            self.current_graph = ext.Solver.path(self.current_graph)

        true_false = [True, False]

        while 0.001 < self.temperature:
            for i in range(0, 100):
                x = random.randint(0, self.row_length - 1)
                y = random.randint(0, self.row_length - 1)
                move_type = self.adjacency_matrix[x][y]

                if not self.change(x, y, move_type):
                    continue

                if not self.evaluate_move():
                    self.revert_change(x, y, move_type)
                else:
                    self.save_change(x, y, move_type)
                self.energy_cost = self.get_energy(self.current_graph)

            self.update_temperature()

        return self.current_graph

    def solve_by_changes_only(self):
        if not nx.is_connected(self.current_graph):
            self.current_graph = ext.Solver.path(self.current_graph)

        nodes = list(self.current_graph.nodes)

        while 0.001 < self.temperature:
            for i in range(0, 200):
                origin = random.choice(nodes)
                edge = random.choice(list(self.current_graph.edges(origin)))
                old_dest = edge[1]

                new_dest = random.choice(nodes)

                if origin == new_dest or old_dest == new_dest or self.current_graph.has_edge(origin, new_dest):
                    continue

                self.move_edge(origin, old_dest, new_dest)

                still_connected = ext.Analytics.is_nodes_connected(self.current_graph, origin, old_dest)
                if still_connected is False:
                    revert_change = True
                else:
                    revert_change = self.evaluate_move() is False

                if revert_change:
                    self.move_edge(origin, new_dest, old_dest)

            self.update_temperature()
            self.energy_cost = self.get_energy(self.current_graph)
        return self.current_graph

    def change(self, x, y, move_type):
        if x == y:
            return False
        if move_type == 1:
            self.current_graph.remove_edge(x, y)
            if ext.Analytics.is_nodes_connected(self.current_graph, x, y):
                return True
            else:
                ext.Creator.add_weighted_edge(self.current_graph, x, y)
                return False
        if move_type == 0:
            ext.Creator.add_weighted_edge(self.current_graph, x, y)
            return True

    def evaluate_move(self):
        new_energy_cost = self.get_energy(self.current_graph)

        if new_energy_cost < self.energy_cost:
            return True

        e = math.exp(-(new_energy_cost - self.energy_cost) / self.temperature)
        if random.uniform(0, 1) < e:
            return True

        return False

    def revert_change(self, x, y, move_type):
        if move_type == 0:
            self.current_graph.remove_edge(x, y)
        else:
            ext.Creator.add_weighted_edge(self.current_graph, x, y)

    def save_change(self, x, y, move_type):
        if move_type == 0:
            self.adjacency_matrix[x][y] = 1
            self.adjacency_matrix[y][x] = 1
            self.energy_cost = self.get_energy(self.current_graph)

        if move_type == 1:
            self.adjacency_matrix[x][y] = 0
            self.adjacency_matrix[y][x] = 0
            self.energy_cost = self.get_energy(self.current_graph)

    temp_iterations = 0

    def update_temperature(self):
        self.temperature = self.temperature * 0.92
        self.temp_iterations += 1
        if self.temp_iterations > 10:
            print("Temp: " + str(self.temperature))
            print("Energy: " + str(self.energy_cost))
            print("Converge: " + str(ext.Analytics.convergence_rate(self.current_graph)))
            self.temp_iterations = 0
            ext.Visual.draw(self.current_graph)

    def get_energy(self, g):
        convergence_rate = ext.Analytics.convergence_rate(g)
        edge_cost = ext.Analytics.total_edge_cost(g)
        edge_percentage = edge_cost / self.max_energy_cost
        return edge_cost
        if convergence_rate == 1.0:
            return math.inf
        return edge_cost / (-math.log(convergence_rate))

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def move_edge(self, origin, old_dest, new_dest):
        if origin == new_dest or old_dest == new_dest:
            return False
        if not self.current_graph.has_edge(origin, old_dest):
            return False
        if self.current_graph.has_edge(origin, new_dest):
            return False

        self.current_graph.remove_edge(origin, old_dest)
        ext.Creator.add_weighted_edge(self.current_graph, origin, new_dest)