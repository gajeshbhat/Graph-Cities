from Graph import Graph
import pprint


def run_tests():
    graph = Graph()

    # You do not need to change anything below this line.
    # You only need to implement Graph.dfs_helper and Graph.bfs

    graph.set_node_names(('Mountain View',  # 0
                          'San Francisco',  # 1
                          'London',  # 2
                          'Shanghai',  # 3
                          'Berlin',  # 4
                          'Sao Paolo',  # 5
                          'Bangalore'))  # 6

    # Connect Cities
    graph.insert_edge(51, 0, 1)  # MV <-> SF
    graph.insert_edge(51, 1, 0)  # SF <-> MV
    graph.insert_edge(9950, 0, 3)  # MV <-> Shanghai
    graph.insert_edge(9950, 3, 0)  # Shanghai <-> MV
    graph.insert_edge(10375, 0, 5)  # MV <-> Sao Paolo
    graph.insert_edge(10375, 5, 0)  # Sao Paolo <-> MV
    graph.insert_edge(9900, 1, 3)  # SF <-> Shanghai
    graph.insert_edge(9900, 3, 1)  # Shanghai <-> SF
    graph.insert_edge(9130, 1, 4)  # SF <-> Berlin
    graph.insert_edge(9130, 4, 1)  # Berlin <-> SF
    graph.insert_edge(9217, 2, 3)  # London <-> Shanghai
    graph.insert_edge(9217, 3, 2)  # Shanghai <-> London
    graph.insert_edge(932, 2, 4)  # London <-> Berlin
    graph.insert_edge(932, 4, 2)  # Berlin <-> London
    graph.insert_edge(9471, 2, 5)  # London <-> Sao Paolo
    graph.insert_edge(9471, 5, 2)  # Sao Paolo <-> London

    # (6) 'Bangalore' is intentionally disconnected (no edges)
    # for this problem and should produce None in the
    # Adjacency List, etc.

    pp = pprint.PrettyPrinter(indent=2)

    print
    "Edge List"
    pp.pprint(graph.get_edge_list_names())

    print
    "\nAdjacency List"
    pp.pprint(graph.get_adjacency_list_names())

    print
    "\nAdjacency Matrix"
    pp.pprint(graph.get_adjacency_matrix())

    print
    "\nDepth First Search"
    pp.pprint(graph.dfs_names(2))

    # Should print:
    # Depth First Search
    # ['London', 'Shanghai', 'Mountain View', 'San Francisco', 'Berlin', 'Sao Paolo']

    print
    "\nBreadth First Search"
    pp.pprint(graph.bfs_names(2))
    # test error reporting
    # pp.pprint(['Sao Paolo', 'Mountain View', 'San Francisco', 'London', 'Shanghai', 'Berlin'])

    # Should print:
    # Breadth First Search
    # ['London', 'Shanghai', 'Berlin', 'Sao Paolo', 'Mountain View', 'San Francisco']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_tests()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
