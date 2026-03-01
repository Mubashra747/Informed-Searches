# Dynamic Pathfinding Agent

A Python-based interactive visualization tool for pathfinding algorithms with dynamic obstacle generation and real-time re-planning capabilities. Built with Pygame for educational purposes and algorithm demonstration.

##  Overview

This project implements **A\* (A-Star)** and **Greedy Best-First Search (GBFS)** pathfinding algorithms with a graphical user interface that visualizes the search process step-by-step. The unique feature is **dynamic obstacle spawning** during agent movement, requiring real-time path re-planning.

**Key Highlights:**
- Step-by-step visualization of algorithm exploration
- Dynamic obstacles spawn while agent is moving
- Automatic path re-planning when obstacles block the route
- Interactive grid editing for custom scenarios
- User-configurable start and goal positions
- Support for Manhattan and Euclidean heuristics

---

## Features

### Core Features
- ✅ **Two Search Algorithms**: A* and Greedy Best-First Search
- ✅ **Two Heuristic Functions**: Manhattan Distance and Euclidean Distance
- ✅ **Dynamic Obstacle Spawning**: Random obstacles appear during agent movement
- ✅ **Real-time Re-planning**: Agent recalculates path when blocked
- ✅ **Interactive Map Editor**: Click to add/remove obstacles
- ✅ **User-defined Start/Goal**: Set custom positions for pathfinding
- ✅ **Step-by-step Visualization**: Watch algorithms "flood" the grid
- ✅ **Random Map Generation**: Create random obstacle layouts (30% density)

### Visualization
- **Frontier Nodes** (Yellow): Nodes in the priority queue waiting to be explored
- **Visited Nodes** (Red): Nodes that have been examined by the algorithm
- **Final Path** (Purple): The optimal route from start to goal
- **Start Node** (Green): Starting position
- **Goal Node** (Blue): Target destination
- **Obstacles** (Brown): Static walls that block movement
- **Empty Cells** (White): Unexplored, traversable cells

---

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Install Python
Download and install Python from [python.org](https://www.python.org/downloads/)

### Step 2: Install Dependencies
```bash
pip install pygame
```

### Step 3: Download the Code
Save the provided code as `pathfinding.py`

### Step 4: Run the Program
```bash
python pathfinding.py
```

## 📖 Usage

### Starting the Program

1. **Run the script:**
   ```bash
   python pathfinding.py
   ```

2. **Enter grid dimensions** when prompted:
   ```
   Enter number of rows: 20
   Enter number of columns: 30
   ```

3. The GUI window will open with:
   - Grid on the left (for visualization)
   - Control panel on the right (with buttons)

### Basic Workflow

1. **Configure Algorithm Settings**
   - Click **"Algorithm: A*"** or **"Algorithm: GBFS"**
   - Click **"Heuristic: Manhattan"** or **"Heuristic: Euclidean"**

2. **Set Start and Goal (Optional)**
   - Click **"Set Start (S)"** button → Click on grid to place start
   - Click **"Set Goal (G)"** button → Click on grid to place goal
   - Default: Start at top-left (0,0), Goal at bottom-right

3. **Create Obstacles**
   - **Left-click** on grid cells to toggle obstacles
   - **Right-click** to remove obstacles
   - Click **"Random Map (30%)"** for automatic obstacle generation
   - Click **"Clear Obstacles"** to remove all walls

4. **Start Pathfinding**
   - Click **"START SEARCH"** to begin
   - Watch the algorithm visualize in real-time:
     - Yellow cells = Frontier (nodes being considered)
     - Red cells = Visited (nodes already explored)
     - Purple cells = Final path

5. **Dynamic Mode**
   - During agent movement, obstacles spawn randomly (3% probability per step)
   - If an obstacle blocks the path, agent stops and re-plans
   - Agent continues from current position to goal

6. **Reset**
   - Click **"Reset Grid"** to clear everything and start fresh

---

## 🧠 Algorithms

### 1. A\* (A-Star) Search

**Formula:** `f(n) = g(n) + h(n)`

- **g(n)**: Actual cost from start to node n
- **h(n)**: Estimated cost from node n to goal (heuristic)
- **f(n)**: Total estimated cost

**Characteristics:**
- ✅ **Optimal**: Always finds the shortest path
- ✅ **Complete**: Will find a path if one exists
- ⚡ **Efficient**: Uses heuristic to guide search
- 📊 **Balanced**: Considers both distance traveled and remaining distance

**Best for:** Finding the absolute shortest path

---

### 2. Greedy Best-First Search (GBFS)

**Formula:** `f(n) = h(n)`

- **h(n)**: Estimated cost from node n to goal (heuristic only)
- Ignores the actual distance traveled

**Characteristics:**
- ⚠️ **Non-optimal**: May not find the shortest path
- ✅ **Complete**: Will find a path if one exists
- ⚡ **Fast**: Often explores fewer nodes
- 🎯 **Goal-directed**: Aggressively moves toward target

**Best for:** Quick pathfinding when optimality is not critical

---

### Heuristic Functions

#### Manhattan Distance
```
h(n) = |x₁ - x₂| + |y₁ - y₂|
```
- **Use case**: Grid-based movement (4-directional: up, down, left, right)
- **Properties**: Admissible (never overestimates)
- **Performance**: Fast to compute

#### Euclidean Distance
```
h(n) = √[(x₂ - x₁)² + (y₂ - y₁)²]
```
- **Use case**: Straight-line distance
- **Properties**: Admissible (never overestimates)
- **Performance**: Slightly more expensive to compute

---

# Color Scheme

| Color | Meaning | RGB Code |
|-------|---------|----------|
|  **Green** | Start Point (S) | (0, 255, 0) |
|  **Blue** | Goal/Target Point (T) | (0, 0, 255) |
|  **Yellow** | Frontier Nodes (in queue) | (255, 255, 0) |
|  **Red** | Visited/Explored Nodes | (255, 0, 0) |
|  **Purple** | Final Successful Path | (128, 0, 128) |
|  **Brown** | Static Obstacle Walls | (139, 69, 19) |
|  **White** | Unexplored Empty Cells | (255, 255, 255) |

---

## 🎮 Controls

### Mouse Controls

| Action | Control |
|--------|---------|
| Toggle obstacle | **Left-click** on grid cell |
| Remove obstacle | **Right-click** on grid cell |
| Set start position | Click **"Set Start (S)"** → Click on grid |
| Set goal position | Click **"Set Goal (G)"** → Click on grid |

### Button Controls

| Button | Function |
|--------|----------|
| **Algorithm: A*** | Select A* search algorithm |
| **Algorithm: GBFS** | Select Greedy Best-First Search |
| **Heuristic: Manhattan** | Use Manhattan distance heuristic |
| **Heuristic: Euclidean** | Use Euclidean distance heuristic |
| **Set Start (S)** | Enable start position selection mode |
| **Set Goal (G)** | Enable goal position selection mode |
| **Random Map (30%)** | Generate random obstacles (30% density) |
| **Clear Obstacles** | Remove all obstacles from grid |
| **START SEARCH** | Begin pathfinding with current settings |
| **Reset Grid** | Clear entire grid (obstacles, paths, etc.) |

---

## ⚙️ Configuration

### Adjustable Parameters

You can modify these variables at the top of the code:

```python
# Grid dimensions (set at runtime via input)
ROWS = 20  # Number of rows
COLS = 30  # Number of columns

# Visualization speed (milliseconds)
VISUALIZATION_DELAY = 20  # Lower = faster, Higher = slower

# Window dimensions
WIDTH = 1100   # Total window width
HEIGHT = 650   # Total window height
GRID_AREA = 650  # Grid area size

# Dynamic obstacle probability
# In dynamic_search() function:
if random.random() < 0.03:  # 3% chance per step
```

### Speed Settings

| Delay (ms) | Speed | Use Case |
|------------|-------|----------|
| 0 | Instant | No visualization, immediate result |
| 10 | Very Fast | Quick demo |
| 20 | **Default** | Balanced visualization |
| 50 | Slow | Easier to follow step-by-step |
| 100 | Very Slow | Detailed educational viewing |


```

### Code Organization

```python
# 1. INITIALIZATION
- Pygame setup
- Grid input
- Window configuration

# 2. CLASSES
- Button: UI button component
- Node: Grid cell with pathfinding properties

# 3. HEURISTICS
- manhattan(): Manhattan distance calculation
- euclidean(): Euclidean distance calculation

# 4. GRID FUNCTIONS
- create_grid(): Initialize grid
- draw_grid(): Render grid lines
- clear_search(): Reset search states
- random_obstacles(): Generate obstacles

# 5. ALGORITHMS
- astar(): A* search implementation
- gbfs(): Greedy Best-First Search implementation
- dynamic_search(): Main search with re-planning

# 6. VISUALIZATION
- draw_all(): Render all components
- reconstruct_path(): Build final path

# 7. MAIN LOOP
- main(): Application entry point

### Algorithm Complexity

**A\* Search:**
- **Time Complexity**: O(b^d) where b = branching factor, d = depth
- **Space Complexity**: O(b^d)
- **Optimality**: Yes (with admissible heuristic)

**Greedy Best-First Search:**
- **Time Complexity**: O(b^m) where m = maximum depth
- **Space Complexity**: O(b^m)
- **Optimality**: No (can find suboptimal paths)

### Movement

- **Direction**: 4-directional (Up, Down, Left, Right)
- **Cost**: Uniform cost of 1 per step
- **Diagonal Movement**: Not supported (can be added)


### Learning Outcomes

After using this project, students should understand:

1. How A* balances exploration and exploitation
2. Why GBFS is faster but non-optimal
3. The role of heuristics in guiding search
4. How dynamic environments require adaptive algorithms
5. The trade-off between optimality and speed

## 📚 References

1. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. IEEE Transactions on Systems Science and Cybernetics.

2. Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.

3. Amit Patel. (n.d.). Introduction to A*. Red Blob Games. https://www.redblobgames.com/pathfinding/a-star/introduction.html
