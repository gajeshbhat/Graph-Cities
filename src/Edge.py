from __future__ import annotations

from typing import Any


class Edge:
    """Represents an edge in a graph connecting two nodes with a weight/value."""

    def __init__(self, value: Any, node_from: 'Node', node_to: 'Node') -> None:
        """Initialize an edge with a value connecting two nodes.

        Args:
            value: The weight/value of this edge (e.g., distance, cost)
            node_from: The source node
            node_to: The destination node
        """
        self.value: Any = value
        self.node_from: 'Node' = node_from
        self.node_to: 'Node' = node_to

    def __str__(self) -> str:
        """Return string representation of the edge."""
        return f"Edge({self.node_from.value} -> {self.node_to.value}, weight={self.value})"

    def __repr__(self) -> str:
        """Return detailed string representation of the edge."""
        return f"Edge(value={self.value}, from={self.node_from.value}, to={self.node_to.value})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on edge properties."""
        if not isinstance(other, Edge):
            return NotImplemented
        return (self.value == other.value and
                self.node_from == other.node_from and
                self.node_to == other.node_to)

    def get_other_node(self, node: 'Node') -> 'Node':
        """Get the other node connected by this edge.

        Args:
            node: One of the nodes connected by this edge

        Returns:
            The other node connected by this edge

        Raises:
            ValueError: If the provided node is not connected by this edge
        """
        if node == self.node_from:
            return self.node_to
        elif node == self.node_to:
            return self.node_from
        else:
            raise ValueError(f"Node {node} is not connected by this edge")
