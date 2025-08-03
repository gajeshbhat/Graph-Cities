"""
Comprehensive unit tests for the Graph Cities project.

This module contains tests for Node, Edge, and Graph classes,
covering all functionality including traversal algorithms and shortest paths.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from typing import List, Any

from src.Node import Node
from src.Edge import Edge
from src.Graph import Graph


class TestNode:
    """Test cases for the Node class."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = Node(5)
        assert node.value == 5
        assert node.edges == []
        assert node.visited is False
    
    def test_node_string_representation(self):
        """Test string representations of nodes."""
        node = Node(42)
        assert str(node) == "Node(42)"
        assert "Node(value=42" in repr(node)
        assert "edges=0" in repr(node)
        assert "visited=False" in repr(node)
    
    def test_node_equality(self):
        """Test node equality comparison."""
        node1 = Node(5)
        node2 = Node(5)
        node3 = Node(10)
        
        assert node1 == node2
        assert node1 != node3
        assert node1 != "not a node"
    
    def test_node_hashable(self):
        """Test that nodes can be used in sets and as dict keys."""
        node1 = Node(5)
        node2 = Node(5)
        node3 = Node(10)
        
        node_set = {node1, node2, node3}
        assert len(node_set) == 2  # node1 and node2 should be considered equal
        
        node_dict = {node1: "value1", node3: "value2"}
        assert len(node_dict) == 2


class TestEdge:
    """Test cases for the Edge class."""
    
    def test_edge_creation(self):
        """Test basic edge creation."""
        node1 = Node(1)
        node2 = Node(2)
        edge = Edge(100, node1, node2)
        
        assert edge.value == 100
        assert edge.node_from == node1
        assert edge.node_to == node2
    
    def test_edge_string_representation(self):
        """Test string representations of edges."""
        node1 = Node(1)
        node2 = Node(2)
        edge = Edge(100, node1, node2)
        
        assert str(edge) == "Edge(1 -> 2, weight=100)"
        assert "Edge(value=100, from=1, to=2)" == repr(edge)
    
    def test_edge_equality(self):
        """Test edge equality comparison."""
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        
        edge1 = Edge(100, node1, node2)
        edge2 = Edge(100, node1, node2)
        edge3 = Edge(200, node1, node2)
        edge4 = Edge(100, node1, node3)
        
        assert edge1 == edge2
        assert edge1 != edge3
        assert edge1 != edge4
        assert edge1 != "not an edge"
    
    def test_get_other_node(self):
        """Test getting the other node connected by an edge."""
        node1 = Node(1)
        node2 = Node(2)
        node3 = Node(3)
        edge = Edge(100, node1, node2)
        
        assert edge.get_other_node(node1) == node2
        assert edge.get_other_node(node2) == node1
        
        with pytest.raises(ValueError, match="Node .* is not connected by this edge"):
            edge.get_other_node(node3)


class TestGraph:
    """Test cases for the Graph class."""
    
    def test_empty_graph_creation(self):
        """Test creating an empty graph."""
        graph = Graph()
        assert graph.nodes == []
        assert graph.edges == []
        assert graph.node_names == []
        assert str(graph) == "Graph(nodes=0, edges=0)"
    
    def test_graph_with_initial_data(self):
        """Test creating a graph with initial nodes and edges."""
        node1 = Node(1)
        node2 = Node(2)
        edge = Edge(100, node1, node2)
        
        graph = Graph([node1, node2], [edge])
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1
    
    def test_insert_node(self):
        """Test inserting nodes into the graph."""
        graph = Graph()
        node = graph.insert_node(5)
        
        assert node.value == 5
        assert node in graph.nodes
        assert graph._node_map[5] == node
        
        # Test inserting duplicate node
        node2 = graph.insert_node(5)
        assert node2 == node  # Should return existing node
        assert len(graph.nodes) == 1
    
    def test_insert_edge(self):
        """Test inserting edges into the graph."""
        graph = Graph()
        edge = graph.insert_edge(100, 1, 2)
        
        assert edge.value == 100
        assert edge in graph.edges
        assert len(graph.nodes) == 2  # Should create nodes automatically
        
        node1 = graph.find_node(1)
        node2 = graph.find_node(2)
        assert edge in node1.edges
        assert edge in node2.edges
    
    def test_set_node_names(self):
        """Test setting node names."""
        graph = Graph()
        names = ('A', 'B', 'C')
        graph.set_node_names(names)
        
        assert graph.node_names == ['A', 'B', 'C']
    
    def test_find_node(self):
        """Test finding nodes by value."""
        graph = Graph()
        graph.insert_node(5)
        
        node = graph.find_node(5)
        assert node is not None
        assert node.value == 5
        
        assert graph.find_node(999) is None
    
    def test_find_max_index(self):
        """Test finding maximum index for matrix representations."""
        graph = Graph()
        assert graph.find_max_index() == 0
        
        # Test with node names
        graph.set_node_names(('A', 'B', 'C'))
        assert graph.find_max_index() == 3
        
        # Test with nodes
        graph = Graph()
        graph.insert_node(5)
        graph.insert_node(10)
        assert graph.find_max_index() == 11  # max value + 1


class TestGraphRepresentations:
    """Test cases for graph representation methods."""
    
    @pytest.fixture
    def sample_graph(self):
        """Create a sample graph for testing."""
        graph = Graph()
        graph.set_node_names(('A', 'B', 'C'))
        graph.insert_edge(10, 0, 1)  # A -> B
        graph.insert_edge(20, 1, 2)  # B -> C
        graph.insert_edge(30, 0, 2)  # A -> C
        return graph
    
    def test_get_edge_list(self, sample_graph):
        """Test getting edge list representation."""
        edge_list = sample_graph.get_edge_list()
        assert len(edge_list) == 3
        assert (10, 0, 1) in edge_list
        assert (20, 1, 2) in edge_list
        assert (30, 0, 2) in edge_list
    
    def test_get_edge_list_names(self, sample_graph):
        """Test getting edge list with names."""
        edge_list = sample_graph.get_edge_list_names()
        assert len(edge_list) == 3
        assert (10, 'A', 'B') in edge_list
        assert (20, 'B', 'C') in edge_list
        assert (30, 'A', 'C') in edge_list
    
    def test_get_edge_list_names_without_names(self):
        """Test error when getting edge list names without setting names."""
        graph = Graph()
        graph.insert_edge(10, 0, 1)
        
        with pytest.raises(ValueError, match="Node names must be set"):
            graph.get_edge_list_names()
    
    def test_get_adjacency_list(self, sample_graph):
        """Test getting adjacency list representation."""
        adj_list = sample_graph.get_adjacency_list()
        assert len(adj_list) == 3
        assert adj_list[0] == [(1, 10), (2, 30)]  # A connects to B and C
        assert adj_list[1] == [(2, 20)]           # B connects to C
        assert adj_list[2] is None                # C connects to nothing (None for empty)
    
    def test_get_adjacency_matrix(self, sample_graph):
        """Test getting adjacency matrix representation."""
        adj_matrix = sample_graph.get_adjacency_matrix()
        assert len(adj_matrix) == 3
        assert len(adj_matrix[0]) == 3
        
        assert adj_matrix[0][1] == 10  # A -> B
        assert adj_matrix[1][2] == 20  # B -> C
        assert adj_matrix[0][2] == 30  # A -> C
        assert adj_matrix[1][0] == 0   # No edge B -> A


if __name__ == '__main__':
    pytest.main([__file__])
