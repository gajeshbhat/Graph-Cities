# Graph Cities 🌐

A clean Python implementation of graph data structures and algorithms using city networks. Features graph representations, traversal algorithms, and shortest path calculations.

## ✨ Features

- **Graph Representations**: Edge lists, adjacency lists, and adjacency matrices
- **Traversal Algorithms**: Depth-First Search (DFS) and Breadth-First Search (BFS)  
- **Shortest Paths**: Dijkstra's algorithm with path reconstruction
- **Graph Analysis**: Connectivity, cycle detection, and statistics
- **Modern Python**: Type hints, error handling, comprehensive tests

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Graph-Cities-1
   ./setup_venv.sh
   ```

2. **Run the demo**:
   ```bash
   source venv/bin/activate
   python examples/main.py
   ```

## 📁 Project Structure

```
Graph-Cities/
├── src/                 # Core graph classes
│   ├── Node.py         # Node implementation
│   ├── Edge.py         # Edge implementation
│   └── Graph.py        # Main graph class
├── examples/           # Demo applications
│   ├── main.py         # Basic demo
│   ├── demo_enhanced.py # Advanced features
│   └── graph_utils.py  # Utility functions
├── tests/              # Unit tests
│   ├── test_graph.py   # Core tests
│   └── test_algorithms.py # Algorithm tests
└── setup_venv.sh       # Setup script
```

## Usage

```python
from src.Graph import Graph

# Create graph
graph = Graph()
graph.set_node_names(('New York', 'Los Angeles', 'Chicago'))

# Add connections (weight, from, to)
graph.insert_edge(2445, 0, 1)  # NY ↔ LA
graph.insert_edge(713, 0, 2)   # NY ↔ Chicago  
graph.insert_edge(1745, 1, 2)  # LA ↔ Chicago

# Traverse
dfs_path = graph.dfs_names(0)  # DFS from NY
bfs_path = graph.bfs_names(0)  # BFS from NY

# Find shortest path
path, distance = graph.shortest_path(0, 1)  # NY to LA
```

## 🧪 Testing

```bash
# Run tests
source venv/bin/activate
pytest tests/

# Run specific test
pytest tests/test_graph.py -v
```

## 🌍 Sample Data

The demo includes major world cities:
- Mountain View ↔ San Francisco (51 miles)
- London ↔ Berlin (932 miles)  
- Shanghai ↔ San Francisco (9,900 miles)
- And more realistic connections...

## 📋 Requirements

- Python 3.8+
- No external dependencies for core functionality
- pytest for testing (optional)

## 🛠️ Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies (optional)
pip install pytest

# Run demo
python examples/main.py
```
