"""
Graph Cities Demo - A demonstration of graph data structures and algorithms.

This module demonstrates various graph representations and traversal algorithms
using a network of cities connected by distances.
"""

from typing import List, Tuple
import pprint

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.Graph import Graph


def create_city_graph() -> Graph:
    """Create and populate a graph with cities and their connections.

    Returns:
        Graph: A populated graph with city connections
    """
    graph = Graph()

    # Set city names (indices 0-6)
    graph.set_node_names((
        'Mountain View',  # 0
        'San Francisco',  # 1
        'London',         # 2
        'Shanghai',       # 3
        'Berlin',         # 4
        'Sao Paolo',      # 5
        'Bangalore'       # 6
    ))

    # Connect cities with distances (bidirectional edges)
    city_connections = [
        (51, 0, 1),      # Mountain View <-> San Francisco
        (51, 1, 0),
        (9950, 0, 3),    # Mountain View <-> Shanghai
        (9950, 3, 0),
        (10375, 0, 5),   # Mountain View <-> Sao Paolo
        (10375, 5, 0),
        (9900, 1, 3),    # San Francisco <-> Shanghai
        (9900, 3, 1),
        (9130, 1, 4),    # San Francisco <-> Berlin
        (9130, 4, 1),
        (9217, 2, 3),    # London <-> Shanghai
        (9217, 3, 2),
        (932, 2, 4),     # London <-> Berlin
        (932, 4, 2),
        (9471, 2, 5),    # London <-> Sao Paolo
        (9471, 5, 2),
    ]

    for distance, from_city, to_city in city_connections:
        graph.insert_edge(distance, from_city, to_city)

    # Note: Bangalore (index 6) is intentionally disconnected
    # to demonstrate handling of isolated nodes

    return graph


def demonstrate_graph_representations(graph: Graph) -> None:
    """Demonstrate different graph representations.

    Args:
        graph: The graph to demonstrate
    """
    pp = pprint.PrettyPrinter(indent=2)

    print("=== GRAPH REPRESENTATIONS ===")

    print("\nEdge List:")
    pp.pprint(graph.get_edge_list_names())

    print("\nAdjacency List:")
    pp.pprint(graph.get_adjacency_list_names())

    print("\nAdjacency Matrix:")
    pp.pprint(graph.get_adjacency_matrix())


def demonstrate_traversal_algorithms(graph: Graph) -> None:
    """Demonstrate graph traversal algorithms.

    Args:
        graph: The graph to traverse
    """
    pp = pprint.PrettyPrinter(indent=2)

    print("\n=== TRAVERSAL ALGORITHMS ===")

    # Start from London (index 2)
    start_city = 2
    start_name = graph.node_names[start_city]

    print(f"\nDepth First Search (starting from {start_name}):")
    dfs_result = graph.dfs_names(start_city)
    pp.pprint(dfs_result)

    print(f"\nBreadth First Search (starting from {start_name}):")
    bfs_result = graph.bfs_names(start_city)
    pp.pprint(bfs_result)


def demonstrate_shortest_path(graph: Graph) -> None:
    """Demonstrate shortest path algorithms.

    Args:
        graph: The graph to analyze
    """
    print("\n=== SHORTEST PATH ALGORITHMS ===")

    try:
        # Find shortest path from London to Mountain View
        start, end = 2, 0  # London to Mountain View
        path, distance = graph.shortest_path(start, end)
        path_names = [graph.node_names[node] for node in path]

        print(f"\nShortest path from {graph.node_names[start]} to {graph.node_names[end]}:")
        print(f"Path: {' -> '.join(path_names)}")
        print(f"Total distance: {distance} miles")

        # Show all shortest distances from London
        print(f"\nAll shortest distances from {graph.node_names[start]}:")
        dijkstra_result = graph.dijkstra(start)
        for node_val, (dist, prev) in dijkstra_result.items():
            if dist != float('inf'):
                print(f"  To {graph.node_names[node_val]}: {dist} miles")
            else:
                print(f"  To {graph.node_names[node_val]}: No path")

    except ValueError as e:
        print(f"Error in shortest path calculation: {e}")


def run_tests() -> None:
    """Run comprehensive tests of the graph implementation."""
    print("Graph Cities Demo")
    print("=" * 50)

    # Create the graph
    graph = create_city_graph()
    print(f"Created graph: {graph}")

    # Demonstrate different aspects
    demonstrate_graph_representations(graph)
    demonstrate_traversal_algorithms(graph)
    demonstrate_shortest_path(graph)

    print("\n" + "=" * 50)
    print("Demo completed successfully!")


def main() -> None:
    """Main entry point of the application."""
    try:
        run_tests()
    except Exception as e:
        print(f"Error running demo: {e}")
        raise


if __name__ == '__main__':
    main()
