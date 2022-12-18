from typing import List
import matplotlib.pyplot as plt
import networkx as nx


def plot_graph(valves: List, filename, full_graph: bool = True):
    labels = {}
    graph = nx.Graph()
    for valve in valves:
        graph.add_node(valve.name)
        labels[valve.name] = valve.name
        if full_graph:
            for connection in valve.connections:
                graph.add_edge(valve.name, connection.name)
        else:
            if valve.parent:
                graph.add_edge(valve.name, valve.parent.name)
    nx.draw_networkx(graph, labels=labels, with_labels=True, node_size=[200 for i in range(len(valves))])
    plt.savefig(f"./graphs/{filename}.png")
    plt.show()
    plt.close()
