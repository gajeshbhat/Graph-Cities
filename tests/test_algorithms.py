"""
Unit tests for graph algorithms including DFS, BFS, and shortest path algorithms.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.Graph import Graph


class TestTraversalAlgorithms:
    """Test cases for graph traversal algorithms."""
    
    @pytest.fixture
    def connected_graph(self):
        """Create a connected graph for testing traversals."""
        graph = Graph()
        graph.set_node_names(('A', 'B', 'C', 'D', 'E'))
        
        # Create a connected graph: A-B-C-D-E with some cross connections
        graph.insert_edge(1, 0, 1)  # A-B
        graph.insert_edge(1, 1, 0)  # B-A (bidirectional)
        graph.insert_edge(2, 1, 2)  # B-C
        graph.insert_edge(2, 2, 1)  # C-B
        graph.insert_edge(3, 2, 3)  # C-D
        graph.insert_edge(3, 3, 2)  # D-C
        graph.insert_edge(4, 3, 4)  # D-E
        graph.insert_edge(4, 4, 3)  # E-D
        graph.insert_edge(5, 0, 2)  # A-C (shortcut)
        graph.insert_edge(5, 2, 0)  # C-A
        
        return graph
    
    @pytest.fixture
    def disconnected_graph(self):
        """Create a graph with disconnected components."""
        graph = Graph()
        graph.set_node_names(('A', 'B', 'C', 'D'))
        
        # Two disconnected components: A-B and C-D
        graph.insert_edge(1, 0, 1)  # A-B
        graph.insert_edge(1, 1, 0)  # B-A
        graph.insert_edge(2, 2, 3)  # C-D
        graph.insert_edge(2, 3, 2)  # D-C
        
        return graph
    
    def test_dfs_connected_graph(self, connected_graph):
        """Test DFS on a connected graph."""
        result = connected_graph.dfs(0)  # Start from A
        
        # Should visit all nodes
        assert len(result) == 5
        assert 0 in result  # A should be first
        assert result[0] == 0
        
        # All nodes should be visited
        assert set(result) == {0, 1, 2, 3, 4}
    
    def test_dfs_names(self, connected_graph):
        """Test DFS with node names."""
        result = connected_graph.dfs_names(0)  # Start from A
        
        assert len(result) == 5
        assert result[0] == 'A'
        assert set(result) == {'A', 'B', 'C', 'D', 'E'}
    
    def test_dfs_nonexistent_node(self, connected_graph):
        """Test DFS with nonexistent starting node."""
        with pytest.raises(ValueError, match="Node .* not found in graph"):
            connected_graph.dfs(999)
    
    def test_dfs_names_without_names(self):
        """Test DFS names without setting node names."""
        graph = Graph()
        graph.insert_edge(1, 0, 1)
        
        with pytest.raises(ValueError, match="Node names must be set"):
            graph.dfs_names(0)
    
    def test_bfs_connected_graph(self, connected_graph):
        """Test BFS on a connected graph."""
        result = connected_graph.bfs(0)  # Start from A
        
        # Should visit all nodes
        assert len(result) == 5
        assert result[0] == 0  # A should be first
        
        # All nodes should be visited
        assert set(result) == {0, 1, 2, 3, 4}
    
    def test_bfs_names(self, connected_graph):
        """Test BFS with node names."""
        result = connected_graph.bfs_names(0)  # Start from A
        
        assert len(result) == 5
        assert result[0] == 'A'
        assert set(result) == {'A', 'B', 'C', 'D', 'E'}
    
    def test_bfs_nonexistent_node(self, connected_graph):
        """Test BFS with nonexistent starting node."""
        with pytest.raises(ValueError, match="Node .* not found in graph"):
            connected_graph.bfs(999)
    
    def test_bfs_names_without_names(self):
        """Test BFS names without setting node names."""
        graph = Graph()
        graph.insert_edge(1, 0, 1)
        
        with pytest.raises(ValueError, match="Node names must be set"):
            graph.bfs_names(0)
    
    def test_dfs_vs_bfs_order(self, connected_graph):
        """Test that DFS and BFS produce valid traversal orders."""
        dfs_result = connected_graph.dfs(0)
        bfs_result = connected_graph.bfs(0)

        # Both should visit all nodes
        assert set(dfs_result) == set(bfs_result)
        assert len(dfs_result) == 5
        assert len(bfs_result) == 5

        # Both should start with the same node
        assert dfs_result[0] == 0
        assert bfs_result[0] == 0
    
    def test_disconnected_graph_traversal(self, disconnected_graph):
        """Test traversal on disconnected graph."""
        # Starting from A should only reach A and B
        dfs_result = disconnected_graph.dfs(0)  # Start from A
        assert set(dfs_result) == {0, 1}  # Only A and B
        
        bfs_result = disconnected_graph.bfs(0)  # Start from A
        assert set(bfs_result) == {0, 1}  # Only A and B
        
        # Starting from C should only reach C and D
        dfs_result = disconnected_graph.dfs(2)  # Start from C
        assert set(dfs_result) == {2, 3}  # Only C and D


class TestShortestPathAlgorithms:
    """Test cases for shortest path algorithms."""
    
    @pytest.fixture
    def weighted_graph(self):
        """Create a weighted graph for shortest path testing."""
        graph = Graph()
        graph.set_node_names(('A', 'B', 'C', 'D'))
        
        # Create a graph with different path costs
        graph.insert_edge(1, 0, 1)   # A-B: cost 1
        graph.insert_edge(10, 0, 2)  # A-C: cost 10
        graph.insert_edge(1, 1, 3)   # B-D: cost 1
        graph.insert_edge(1, 2, 3)   # C-D: cost 1
        
        return graph
    
    def test_dijkstra_basic(self, weighted_graph):
        """Test basic Dijkstra's algorithm functionality."""
        result = weighted_graph.dijkstra(0)  # Start from A

        # Check distances
        assert result[0] == (0, None)    # A: distance 0, no previous
        assert result[1] == (1, 0)       # B: distance 1, previous A
        assert result[2] == (3, 3)       # C: distance 3, previous D (A->B->D->C is shorter)
        assert result[3] == (2, 1)       # D: distance 2, previous B (A->B->D)
    
    def test_dijkstra_nonexistent_node(self, weighted_graph):
        """Test Dijkstra with nonexistent starting node."""
        with pytest.raises(ValueError, match="Node .* not found in graph"):
            weighted_graph.dijkstra(999)
    
    def test_shortest_path_basic(self, weighted_graph):
        """Test basic shortest path functionality."""
        path, distance = weighted_graph.shortest_path(0, 3)  # A to D
        
        assert path == [0, 1, 3]  # A -> B -> D
        assert distance == 2
    
    def test_shortest_path_same_node(self, weighted_graph):
        """Test shortest path from node to itself."""
        path, distance = weighted_graph.shortest_path(0, 0)  # A to A
        
        assert path == [0]
        assert distance == 0
    
    def test_shortest_path_nonexistent_nodes(self, weighted_graph):
        """Test shortest path with nonexistent nodes."""
        with pytest.raises(ValueError, match="Start node .* not found"):
            weighted_graph.shortest_path(999, 0)
        
        with pytest.raises(ValueError, match="End node .* not found"):
            weighted_graph.shortest_path(0, 999)
    
    def test_shortest_path_no_path(self):
        """Test shortest path when no path exists."""
        graph = Graph()
        graph.set_node_names(('A', 'B'))
        graph.insert_node(0)  # A (isolated)
        graph.insert_node(1)  # B (isolated)
        
        with pytest.raises(ValueError, match="No path exists"):
            graph.shortest_path(0, 1)
    
    def test_complex_shortest_path(self):
        """Test shortest path on a more complex graph."""
        graph = Graph()
        graph.set_node_names(('A', 'B', 'C', 'D', 'E'))
        
        # Create a graph where the direct path is not the shortest
        graph.insert_edge(10, 0, 4)  # A-E: cost 10 (direct but expensive)
        graph.insert_edge(2, 0, 1)   # A-B: cost 2
        graph.insert_edge(2, 1, 2)   # B-C: cost 2
        graph.insert_edge(2, 2, 3)   # C-D: cost 2
        graph.insert_edge(2, 3, 4)   # D-E: cost 2
        
        path, distance = graph.shortest_path(0, 4)  # A to E
        
        assert path == [0, 1, 2, 3, 4]  # A -> B -> C -> D -> E
        assert distance == 8  # 2+2+2+2 = 8 (cheaper than direct cost of 10)


class TestGraphUtilities:
    """Test cases for graph utility methods."""
    
    def test_clear_visited(self):
        """Test clearing visited status of nodes."""
        graph = Graph()
        graph.insert_edge(1, 0, 1)
        
        # Mark nodes as visited
        for node in graph.nodes:
            node.visited = True
        
        # Clear visited status
        graph._clear_visited()
        
        # All nodes should be unvisited
        for node in graph.nodes:
            assert node.visited is False


if __name__ == '__main__':
    pytest.main([__file__])
