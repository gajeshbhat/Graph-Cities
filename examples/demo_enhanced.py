"""
Enhanced Graph Cities Demo - Showcasing all advanced features.

This demo showcases the enhanced functionality including graph analysis,
statistics, and utility functions.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import List
from src.Graph import Graph
from examples.graph_utils import (
    print_graph_stats, 
    print_adjacency_list_formatted,
    print_shortest_paths_table,
    print_connected_components,
    create_simple_text_visualization,
    analyze_graph_comprehensive
)


def create_sample_graphs() -> List[Graph]:
    """Create various sample graphs for demonstration."""
    graphs = []
    
    # 1. Connected graph with cycle
    print("Creating connected graph with cycle...")
    graph1 = Graph()
    graph1.set_node_names(('A', 'B', 'C', 'D'))
    graph1.insert_edge(1, 0, 1)  # A-B
    graph1.insert_edge(1, 1, 0)  # B-A
    graph1.insert_edge(2, 1, 2)  # B-C
    graph1.insert_edge(2, 2, 1)  # C-B
    graph1.insert_edge(3, 2, 3)  # C-D
    graph1.insert_edge(3, 3, 2)  # D-C
    graph1.insert_edge(4, 3, 0)  # D-A (creates cycle)
    graph1.insert_edge(4, 0, 3)  # A-D
    graphs.append(("Connected Graph with Cycle", graph1))
    
    # 2. Disconnected graph
    print("Creating disconnected graph...")
    graph2 = Graph()
    graph2.set_node_names(('X', 'Y', 'Z', 'W'))
    graph2.insert_edge(1, 0, 1)  # X-Y
    graph2.insert_edge(1, 1, 0)  # Y-X
    graph2.insert_edge(2, 2, 3)  # Z-W
    graph2.insert_edge(2, 3, 2)  # W-Z
    graphs.append(("Disconnected Graph", graph2))
    
    # 3. Tree (connected, no cycles)
    print("Creating tree graph...")
    graph3 = Graph()
    graph3.set_node_names(('Root', 'Left', 'Right', 'LeftLeft', 'LeftRight'))
    graph3.insert_edge(1, 0, 1)  # Root-Left
    graph3.insert_edge(1, 1, 0)  # Left-Root
    graph3.insert_edge(2, 0, 2)  # Root-Right
    graph3.insert_edge(2, 2, 0)  # Right-Root
    graph3.insert_edge(3, 1, 3)  # Left-LeftLeft
    graph3.insert_edge(3, 3, 1)  # LeftLeft-Left
    graph3.insert_edge(4, 1, 4)  # Left-LeftRight
    graph3.insert_edge(4, 4, 1)  # LeftRight-Left
    graphs.append(("Tree Graph (No Cycles)", graph3))
    
    return graphs


def demonstrate_graph_analysis(graph: Graph, name: str) -> None:
    """Demonstrate comprehensive graph analysis."""
    print(f"\n{'='*60}")
    print(f"📊 ANALYZING: {name}")
    print(f"{'='*60}")
    
    # Basic info
    print(f"Graph: {graph}")
    
    # Statistics
    print_graph_stats(graph)
    print()
    
    # Connectivity analysis
    print("🔗 Connectivity Analysis")
    print("-" * 30)
    print(f"Connected: {'Yes' if graph.is_connected() else 'No'}")
    print(f"Has Cycle: {'Yes' if graph.has_cycle() else 'No'}")
    
    components = graph.get_connected_components()
    print(f"Connected Components: {len(components)}")
    for i, component in enumerate(components, 1):
        if graph.node_names:
            comp_names = [graph.node_names[node] for node in component]
            print(f"  Component {i}: {', '.join(comp_names)}")
        else:
            print(f"  Component {i}: {component}")
    print()
    
    # Node degrees
    print("📈 Node Degrees")
    print("-" * 20)
    for node in graph.nodes:
        degree = graph.get_node_degree(node.value)
        node_name = graph.node_names[node.value] if graph.node_names else f"Node {node.value}"
        print(f"  {node_name}: {degree}")
    print()
    
    # Traversals from first node
    if graph.nodes:
        start_node = graph.nodes[0].value
        start_name = graph.node_names[start_node] if graph.node_names else f"Node {start_node}"
        
        print(f"🚶 Traversals from {start_name}")
        print("-" * 30)
        try:
            dfs_result = graph.dfs_names(start_node) if graph.node_names else graph.dfs(start_node)
            bfs_result = graph.bfs_names(start_node) if graph.node_names else graph.bfs(start_node)
            
            print(f"DFS: {' → '.join(map(str, dfs_result))}")
            print(f"BFS: {' → '.join(map(str, bfs_result))}")
        except Exception as e:
            print(f"Traversal error: {e}")
        print()
        
        # Shortest paths
        print(f"🛣️  Shortest Paths from {start_name}")
        print("-" * 40)
        try:
            dijkstra_result = graph.dijkstra(start_node)
            for node_val, (distance, _) in dijkstra_result.items():
                dest_name = graph.node_names[node_val] if graph.node_names else f"Node {node_val}"
                if distance == float('inf'):
                    print(f"  To {dest_name}: No path")
                else:
                    print(f"  To {dest_name}: {distance}")
        except Exception as e:
            print(f"Shortest path error: {e}")


def main() -> None:
    """Main demonstration function."""
    print("🌐 Enhanced Graph Cities Demo")
    print("=" * 60)
    print("This demo showcases advanced graph analysis features")
    print("=" * 60)
    
    # Create sample graphs
    sample_graphs = create_sample_graphs()
    
    # Analyze each graph
    for name, graph in sample_graphs:
        demonstrate_graph_analysis(graph, name)
    
    print("\n" + "="*60)
    print("🎯 COMPREHENSIVE ANALYSIS OF CITY GRAPH")
    print("="*60)
    
    # Load the main city graph
    from examples.main import create_city_graph
    city_graph = create_city_graph()
    
    # Full analysis
    analyze_graph_comprehensive(city_graph)
    
    print("\n" + "="*60)
    print("✅ Enhanced demo completed successfully!")
    print("="*60)
    
    print("\n📚 What you've seen:")
    print("• Graph connectivity analysis")
    print("• Cycle detection")
    print("• Connected components identification")
    print("• Node degree calculations")
    print("• Graph density metrics")
    print("• Comprehensive traversal algorithms")
    print("• Advanced shortest path analysis")
    print("• Text-based graph visualization")
    
    print("\n🚀 Try creating your own graphs and analyzing them!")


if __name__ == '__main__':
    main()
