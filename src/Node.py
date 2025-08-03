from __future__ import annotations

from typing import List, Any


class Node:
    """Represents a node in a graph with a value and connected edges."""

    def __init__(self, value: Any) -> None:
        """Initialize a node with a value.

        Args:
            value: The value stored in this node (typically an integer ID)
        """
        self.value: Any = value
        self.edges: List['Edge'] = []
        self.visited: bool = False

    def __str__(self) -> str:
        """Return string representation of the node."""
        return f"Node({self.value})"

    def __repr__(self) -> str:
        """Return detailed string representation of the node."""
        return f"Node(value={self.value}, edges={len(self.edges)}, visited={self.visited})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on node value."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        """Make node hashable based on its value."""
        return hash(self.value)
