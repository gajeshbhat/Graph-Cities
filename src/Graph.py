from __future__ import annotations

from typing import List, Optional, Tuple, Any, Dict, Union
from collections import deque
import heapq

from .Node import Node
from .Edge import Edge


class Graph:
    """A graph data structure supporting various representations and algorithms."""

    def __init__(self, nodes: Optional[List[Node]] = None, edges: Optional[List[Edge]] = None) -> None:
        """Initialize a graph with optional nodes and edges.

        Args:
            nodes: Initial list of nodes (default: empty list)
            edges: Initial list of edges (default: empty list)
        """
        self.nodes: List[Node] = nodes or []
        self.edges: List[Edge] = edges or []
        self.node_names: List[str] = []
        self._node_map: Dict[Any, Node] = {}

    def set_node_names(self, names: Tuple[str, ...]) -> None:
        """Set names for nodes where the Nth name corresponds to node number N.

        Args:
            names: Tuple of node names (node numbers are 0-based)
        """
        self.node_names = list(names)

    def insert_node(self, new_node_val: Any) -> Node:
        """Insert a new node with the given value.

        Args:
            new_node_val: Value for the new node

        Returns:
            The newly created node
        """
        if new_node_val in self._node_map:
            return self._node_map[new_node_val]

        new_node = Node(new_node_val)
        self.nodes.append(new_node)
        self._node_map[new_node_val] = new_node
        return new_node

    def insert_edge(self, new_edge_val: Any, node_from_val: Any, node_to_val: Any) -> Edge:
        """Insert a new edge, creating new nodes if necessary.

        Args:
            new_edge_val: Weight/value of the edge
            node_from_val: Value of the source node
            node_to_val: Value of the destination node

        Returns:
            The newly created edge
        """
        # Find or create nodes
        node_from = self._node_map.get(node_from_val) or self.insert_node(node_from_val)
        node_to = self._node_map.get(node_to_val) or self.insert_node(node_to_val)

        # Create and add edge
        new_edge = Edge(new_edge_val, node_from, node_to)
        node_from.edges.append(new_edge)
        node_to.edges.append(new_edge)
        self.edges.append(new_edge)
        return new_edge

    def get_edge_list(self) -> List[Tuple[Any, Any, Any]]:
        """Return a list of triples: (Edge Value, From Node, To Node).

        Returns:
            List of tuples containing edge information
        """
        return [(e.value, e.node_from.value, e.node_to.value) for e in self.edges]

    def get_edge_list_names(self) -> List[Tuple[Any, str, str]]:
        """Return a list of triples: (Edge Value, From Node Name, To Node Name).

        Returns:
            List of tuples with edge values and node names

        Raises:
            IndexError: If node names haven't been set or are incomplete
        """
        if not self.node_names:
            raise ValueError("Node names must be set before calling get_edge_list_names()")

        return [(edge.value,
                 self.node_names[edge.node_from.value],
                 self.node_names[edge.node_to.value])
                for edge in self.edges]

    def get_adjacency_list(self) -> List[Optional[List[Tuple[Any, Any]]]]:
        """Return adjacency list representation of the graph.

        The indices of the outer list represent "from" nodes.
        Each section stores a list of tuples: (To Node, Edge Value).
        Empty lists are replaced with None.

        Returns:
            List where each index represents a node and contains its neighbors
        """
        max_index = self.find_max_index()
        adjacency_list: List[List[Tuple[Any, Any]]] = [[] for _ in range(max_index)]

        for edge in self.edges:
            from_value, to_value = edge.node_from.value, edge.node_to.value
            adjacency_list[from_value].append((to_value, edge.value))

        return [neighbors if neighbors else None for neighbors in adjacency_list]

    def get_adjacency_list_names(self) -> List[Optional[List[Tuple[str, Any]]]]:
        """Return adjacency list with node names instead of numbers.

        Each section stores a list of tuples: (To Node Name, Edge Value).
        Node names come from the names set with set_node_names().

        Returns:
            List where each index represents a node and contains named neighbors

        Raises:
            ValueError: If node names haven't been set
        """
        if not self.node_names:
            raise ValueError("Node names must be set before calling get_adjacency_list_names()")

        adjacency_list = self.get_adjacency_list()

        def convert_to_names(pair: Tuple[Any, Any]) -> Tuple[str, Any]:
            node_number, value = pair
            return (self.node_names[node_number], value)

        result = []
        for adjacency_list_for_node in adjacency_list:
            if adjacency_list_for_node is None:
                result.append(None)
            else:
                result.append([convert_to_names(pair) for pair in adjacency_list_for_node])

        return result

    def get_adjacency_matrix(self) -> List[List[Any]]:
        """Return adjacency matrix representation of the graph.

        Row numbers represent from nodes, column numbers represent to nodes.
        Edge values are stored in each spot, 0 if no edge exists.

        Returns:
            2D list representing the adjacency matrix
        """
        max_index = self.find_max_index()
        adjacency_matrix = [[0] * max_index for _ in range(max_index)]

        for edge in self.edges:
            from_index, to_index = edge.node_from.value, edge.node_to.value
            adjacency_matrix[from_index][to_index] = edge.value

        return adjacency_matrix

    def find_max_index(self) -> int:
        """Return the highest node number or length of node names.

        Returns:
            Maximum index needed for matrix/list representations
        """
        if self.node_names:
            return len(self.node_names)

        if not self.nodes:
            return 0

        return max(node.value for node in self.nodes) + 1

    def find_node(self, node_number: Any) -> Optional[Node]:
        """Return the node with the given value.

        Args:
            node_number: Value of the node to find

        Returns:
            Node with the given value, or None if not found
        """
        return self._node_map.get(node_number)

    def _clear_visited(self) -> None:
        """Reset visited status for all nodes."""
        for node in self.nodes:
            node.visited = False

    def dfs_helper(self, start_node: Node) -> List[Any]:
        """Recursive helper for depth-first search.

        Args:
            start_node: The starting node for DFS

        Returns:
            List of traversed node values
        """
        if start_node.visited:
            return []

        result = [start_node.value]
        start_node.visited = True

        # Find outgoing edges (edges where this node is the source)
        for edge in start_node.edges:
            other_node = edge.get_other_node(start_node)
            if not other_node.visited:
                result.extend(self.dfs_helper(other_node))

        return result

    def dfs(self, start_node_num: Any) -> List[Any]:
        """Perform depth-first search starting from the given node.

        Args:
            start_node_num: Value of the starting node

        Returns:
            List of node values in DFS order

        Raises:
            ValueError: If the starting node doesn't exist
        """
        self._clear_visited()
        start_node = self.find_node(start_node_num)

        if start_node is None:
            raise ValueError(f"Node {start_node_num} not found in graph")

        return self.dfs_helper(start_node)

    def dfs_names(self, start_node_num: Any) -> List[str]:
        """Return DFS results with node names instead of numbers.

        Args:
            start_node_num: Value of the starting node

        Returns:
            List of node names in DFS order

        Raises:
            ValueError: If node names haven't been set or starting node doesn't exist
        """
        if not self.node_names:
            raise ValueError("Node names must be set before calling dfs_names()")

        return [self.node_names[num] for num in self.dfs(start_node_num)]

    def bfs(self, start_node_num: Any) -> List[Any]:
        """Perform breadth-first search starting from the given node.

        Args:
            start_node_num: Value of the starting node

        Returns:
            List of node values in BFS order

        Raises:
            ValueError: If the starting node doesn't exist
        """
        start_node = self.find_node(start_node_num)
        if start_node is None:
            raise ValueError(f"Node {start_node_num} not found in graph")

        self._clear_visited()

        result = []
        queue = deque([start_node_num])
        visited_set = {start_node_num}  # Track visited nodes to avoid duplicates

        while queue:
            current_node_num = queue.popleft()
            current_node = self.find_node(current_node_num)

            if current_node and not current_node.visited:
                current_node.visited = True
                result.append(current_node_num)

                # Add unvisited neighbors to queue
                for edge in current_node.edges:
                    neighbor = edge.get_other_node(current_node)
                    if neighbor.value not in visited_set:
                        queue.append(neighbor.value)
                        visited_set.add(neighbor.value)

        return result

    def bfs_names(self, start_node_num: Any) -> List[str]:
        """Return BFS results with node names instead of numbers.

        Args:
            start_node_num: Value of the starting node

        Returns:
            List of node names in BFS order

        Raises:
            ValueError: If node names haven't been set or starting node doesn't exist
        """
        if not self.node_names:
            raise ValueError("Node names must be set before calling bfs_names()")

        return [self.node_names[num] for num in self.bfs(start_node_num)]

    def __str__(self) -> str:
        """Return string representation of the graph."""
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"

    def __repr__(self) -> str:
        """Return detailed string representation of the graph."""
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)}, named={bool(self.node_names)})"

    def dijkstra(self, start_node_num: Any) -> Dict[Any, Tuple[float, Optional[Any]]]:
        """Find shortest paths from start node to all other nodes using Dijkstra's algorithm.

        Args:
            start_node_num: Value of the starting node

        Returns:
            Dictionary mapping node values to (distance, previous_node) tuples

        Raises:
            ValueError: If the starting node doesn't exist
        """
        start_node = self.find_node(start_node_num)
        if start_node is None:
            raise ValueError(f"Node {start_node_num} not found in graph")

        # Initialize distances and previous nodes
        distances: Dict[Any, float] = {node.value: float('inf') for node in self.nodes}
        previous: Dict[Any, Optional[Any]] = {node.value: None for node in self.nodes}
        distances[start_node_num] = 0

        # Priority queue: (distance, node_value)
        pq = [(0, start_node_num)]
        visited = set()

        while pq:
            current_dist, current_node_val = heapq.heappop(pq)

            if current_node_val in visited:
                continue

            visited.add(current_node_val)
            current_node = self.find_node(current_node_val)

            if current_node is None:
                continue

            # Check all neighbors
            for edge in current_node.edges:
                neighbor = edge.get_other_node(current_node)
                if neighbor.value in visited:
                    continue

                # Calculate new distance
                new_dist = current_dist + edge.value

                if new_dist < distances[neighbor.value]:
                    distances[neighbor.value] = new_dist
                    previous[neighbor.value] = current_node_val
                    heapq.heappush(pq, (new_dist, neighbor.value))

        return {node_val: (dist, prev) for node_val, dist, prev in
                zip(distances.keys(), distances.values(), previous.values())}

    def shortest_path(self, start_node_num: Any, end_node_num: Any) -> Tuple[List[Any], float]:
        """Find the shortest path between two nodes.

        Args:
            start_node_num: Value of the starting node
            end_node_num: Value of the ending node

        Returns:
            Tuple of (path as list of node values, total distance)

        Raises:
            ValueError: If either node doesn't exist or no path exists
        """
        if self.find_node(start_node_num) is None:
            raise ValueError(f"Start node {start_node_num} not found in graph")
        if self.find_node(end_node_num) is None:
            raise ValueError(f"End node {end_node_num} not found in graph")

        dijkstra_result = self.dijkstra(start_node_num)
        distance, previous = dijkstra_result[end_node_num]

        if distance == float('inf'):
            raise ValueError(f"No path exists from {start_node_num} to {end_node_num}")

        # Reconstruct path
        path = []
        current = end_node_num
        while current is not None:
            path.append(current)
            current = dijkstra_result[current][1]  # previous node

        path.reverse()
        return path, distance

    def is_connected(self) -> bool:
        """Check if the graph is connected (all nodes reachable from any node).

        Returns:
            True if the graph is connected, False otherwise
        """
        if not self.nodes:
            return True

        # Use DFS from the first node to see if we can reach all nodes
        start_node = self.nodes[0]
        visited_count = len(self.dfs_helper(start_node))
        self._clear_visited()

        return visited_count == len(self.nodes)

    def get_connected_components(self) -> List[List[Any]]:
        """Find all connected components in the graph.

        Returns:
            List of lists, where each inner list contains node values in a component
        """
        self._clear_visited()
        components = []

        for node in self.nodes:
            if not node.visited:
                component = self.dfs_helper(node)
                components.append(component)

        self._clear_visited()
        return components

    def has_cycle(self) -> bool:
        """Check if the graph has a cycle using DFS.

        Returns:
            True if the graph contains a cycle, False otherwise
        """
        self._clear_visited()

        def dfs_cycle_check(node: Node, parent: Optional[Node] = None) -> bool:
            node.visited = True

            for edge in node.edges:
                neighbor = edge.get_other_node(node)

                if not neighbor.visited:
                    if dfs_cycle_check(neighbor, node):
                        return True
                elif neighbor != parent:  # Back edge found (cycle)
                    return True

            return False

        # Check each component
        for node in self.nodes:
            if not node.visited:
                if dfs_cycle_check(node):
                    self._clear_visited()
                    return True

        self._clear_visited()
        return False

    def get_node_degree(self, node_val: Any) -> int:
        """Get the degree (number of connections) of a node.

        Args:
            node_val: Value of the node

        Returns:
            Number of edges connected to the node

        Raises:
            ValueError: If the node doesn't exist
        """
        node = self.find_node(node_val)
        if node is None:
            raise ValueError(f"Node {node_val} not found in graph")

        return len(node.edges)

    def get_graph_density(self) -> float:
        """Calculate the density of the graph (ratio of edges to possible edges).

        Returns:
            Graph density as a float between 0 and 1
        """
        if len(self.nodes) < 2:
            return 0.0

        num_nodes = len(self.nodes)
        max_edges = num_nodes * (num_nodes - 1) // 2  # For undirected graph
        actual_edges = len(self.edges) // 2  # Each edge is counted twice

        return actual_edges / max_edges if max_edges > 0 else 0.0

    def get_graph_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the graph.

        Returns:
            Dictionary containing various graph statistics
        """
        stats = {
            'num_nodes': len(self.nodes),
            'num_edges': len(self.edges) // 2,  # Undirected edges counted twice
            'is_connected': self.is_connected(),
            'has_cycle': self.has_cycle(),
            'density': self.get_graph_density(),
            'connected_components': len(self.get_connected_components())
        }

        if self.nodes:
            degrees = [self.get_node_degree(node.value) for node in self.nodes]
            stats.update({
                'min_degree': min(degrees),
                'max_degree': max(degrees),
                'avg_degree': sum(degrees) / len(degrees)
            })

        return stats
