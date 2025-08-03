"""
Utility functions for graph analysis and visualization.

This module provides additional utilities for working with graphs,
including simple text-based visualization and analysis tools.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Dict, Any, Optional
from src.Graph import Graph


def print_graph_stats(graph: Graph) -> None:
    """Print comprehensive statistics about the graph.
    
    Args:
        graph: The graph to analyze
    """
    stats = graph.get_graph_stats()
    
    print("📊 Graph Statistics")
    print("=" * 40)
    print(f"Nodes: {stats['num_nodes']}")
    print(f"Edges: {stats['num_edges']}")
    print(f"Connected: {'Yes' if stats['is_connected'] else 'No'}")
    print(f"Has Cycle: {'Yes' if stats['has_cycle'] else 'No'}")
    print(f"Density: {stats['density']:.3f}")
    print(f"Connected Components: {stats['connected_components']}")
    
    if 'min_degree' in stats:
        print(f"Min Degree: {stats['min_degree']}")
        print(f"Max Degree: {stats['max_degree']}")
        print(f"Avg Degree: {stats['avg_degree']:.2f}")


def print_adjacency_list_formatted(graph: Graph) -> None:
    """Print a nicely formatted adjacency list.
    
    Args:
        graph: The graph to display
    """
    print("🔗 Adjacency List (Formatted)")
    print("=" * 40)
    
    if not graph.node_names:
        print("Node names not set. Using numeric IDs.")
        adj_list = graph.get_adjacency_list()
        for i, neighbors in enumerate(adj_list):
            if neighbors:
                neighbor_str = ", ".join([f"{n}({w})" for n, w in neighbors])
                print(f"Node {i}: {neighbor_str}")
            else:
                print(f"Node {i}: (isolated)")
    else:
        adj_list = graph.get_adjacency_list_names()
        for i, neighbors in enumerate(adj_list):
            node_name = graph.node_names[i] if i < len(graph.node_names) else f"Node {i}"
            if neighbors:
                neighbor_str = ", ".join([f"{n}({w})" for n, w in neighbors])
                print(f"{node_name}: {neighbor_str}")
            else:
                print(f"{node_name}: (isolated)")


def print_shortest_paths_table(graph: Graph, start_node: Any) -> None:
    """Print a table of shortest paths from a starting node.
    
    Args:
        graph: The graph to analyze
        start_node: Starting node value
    """
    try:
        dijkstra_result = graph.dijkstra(start_node)
        start_name = graph.node_names[start_node] if graph.node_names else f"Node {start_node}"
        
        print(f"🛣️  Shortest Paths from {start_name}")
        print("=" * 50)
        print(f"{'Destination':<15} {'Distance':<10} {'Path'}")
        print("-" * 50)
        
        for node_val, (distance, _) in dijkstra_result.items():
            if distance == float('inf'):
                dest_name = graph.node_names[node_val] if graph.node_names else f"Node {node_val}"
                print(f"{dest_name:<15} {'∞':<10} No path")
            else:
                try:
                    path, _ = graph.shortest_path(start_node, node_val)
                    if graph.node_names:
                        path_names = [graph.node_names[n] for n in path]
                        path_str = " → ".join(path_names)
                        dest_name = graph.node_names[node_val]
                    else:
                        path_str = " → ".join(map(str, path))
                        dest_name = f"Node {node_val}"
                    
                    print(f"{dest_name:<15} {distance:<10} {path_str}")
                except ValueError:
                    dest_name = graph.node_names[node_val] if graph.node_names else f"Node {node_val}"
                    print(f"{dest_name:<15} {'∞':<10} No path")
                    
    except ValueError as e:
        print(f"Error: {e}")


def print_connected_components(graph: Graph) -> None:
    """Print all connected components in the graph.
    
    Args:
        graph: The graph to analyze
    """
    components = graph.get_connected_components()
    
    print("🔗 Connected Components")
    print("=" * 30)
    
    if len(components) == 1:
        print("Graph is fully connected (1 component)")
    else:
        print(f"Graph has {len(components)} connected components:")
        
    for i, component in enumerate(components, 1):
        if graph.node_names:
            component_names = [graph.node_names[node] for node in component]
            component_str = ", ".join(component_names)
        else:
            component_str = ", ".join(map(str, component))
            
        print(f"  Component {i}: {component_str}")


def create_simple_text_visualization(graph: Graph) -> str:
    """Create a simple text-based visualization of the graph.
    
    Args:
        graph: The graph to visualize
        
    Returns:
        String representation of the graph
    """
    if not graph.nodes:
        return "Empty graph"
    
    lines = []
    lines.append("Graph Visualization (Text)")
    lines.append("=" * 30)
    
    # Show nodes and their connections
    for node in graph.nodes:
        node_name = graph.node_names[node.value] if graph.node_names and node.value < len(graph.node_names) else f"Node {node.value}"
        
        if not node.edges:
            lines.append(f"{node_name} (isolated)")
        else:
            connections = []
            for edge in node.edges:
                other_node = edge.get_other_node(node)
                other_name = graph.node_names[other_node.value] if graph.node_names and other_node.value < len(graph.node_names) else f"Node {other_node.value}"
                connections.append(f"{other_name}({edge.value})")
            
            lines.append(f"{node_name} -- {', '.join(connections)}")
    
    return "\n".join(lines)


def analyze_graph_comprehensive(graph: Graph) -> None:
    """Perform comprehensive analysis of the graph and print results.
    
    Args:
        graph: The graph to analyze
    """
    print("🔍 Comprehensive Graph Analysis")
    print("=" * 50)
    print()
    
    # Basic statistics
    print_graph_stats(graph)
    print()
    
    # Adjacency representation
    print_adjacency_list_formatted(graph)
    print()
    
    # Connected components
    print_connected_components(graph)
    print()
    
    # Text visualization
    print(create_simple_text_visualization(graph))
    print()
    
    # Shortest paths from first node (if graph has nodes)
    if graph.nodes:
        first_node = graph.nodes[0].value
        print_shortest_paths_table(graph, first_node)


if __name__ == "__main__":
    # Demo of utility functions
    from examples.main import create_city_graph
    
    print("Graph Utilities Demo")
    print("=" * 50)
    
    graph = create_city_graph()
    analyze_graph_comprehensive(graph)
