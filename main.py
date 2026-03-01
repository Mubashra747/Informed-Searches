import pygame
import heapq
import random

pygame.init()

# ================= USER GRID INPUT =================
ROWS = int(input("Enter number of rows: "))
COLS = int(input("Enter number of columns: "))

WIDTH = 1100
HEIGHT = 750
GRID_AREA = 750
CELL_SIZE = GRID_AREA // max(ROWS, COLS)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding - A* & GBFS")

# ================= COLORS =================
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# ================= NODE =================
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.is_start = False
        self.is_goal = False
        self.is_obstacle = False
        self.neighbors = []

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(WIN, GREY, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

    def make_start(self):
        self.is_start = True
        self.color = GREEN

    def make_goal(self):
        self.is_goal = True
        self.color = BLUE

    def make_obstacle(self):
        if not self.is_start and not self.is_goal:
            self.is_obstacle = True
            self.color = BROWN

    def remove_obstacle(self):
        if not self.is_start and not self.is_goal:
            self.is_obstacle = False
            self.color = WHITE

    def make_path(self):
        if not self.is_start and not self.is_goal:
            self.color = PURPLE

    def make_agent(self):
        if not self.is_start and not self.is_goal:
            self.color = ORANGE

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in directions:
            r = self.row + dr
            c = self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                if not grid[r][c].is_obstacle:
                    self.neighbors.append(grid[r][c])

# ================= HEURISTIC =================
def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

# ================= PATH RECONSTRUCTION =================
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# ================= A* =================
def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, goal)

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None

# ================= GBFS =================
def gbfs(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, goal)

        visited.add(current)

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))

    return None

# ================= MAIN =================
def main():
    grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
    start = grid[0][0]
    goal = grid[ROWS-1][COLS-1]
    start.make_start()
    goal.make_goal()

    agent_pos = start
    current_path = []
    algorithm = None

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(5)
        WIN.fill(WHITE)

        for row in grid:
            for node in row:
                node.update_neighbors(grid)
                node.draw()

        pygame.display.update()

        # Agent Movement
        if current_path:
            next_node = current_path.pop(0)

            # If blocked → Replan
            if next_node.is_obstacle:
                if algorithm == "astar":
                    current_path = astar(grid, agent_pos, goal) or []
                else:
                    current_path = gbfs(grid, agent_pos, goal) or []
                continue

            agent_pos.color = WHITE if not agent_pos.is_start else GREEN
            agent_pos = next_node
            agent_pos.make_agent()

            # Random Dynamic Obstacle
            if random.random() < 0.2:
                r = random.randint(0, ROWS-1)
                c = random.randint(0, COLS-1)
                grid[r][c].make_obstacle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    algorithm = "astar"
                    current_path = astar(grid, agent_pos, goal) or []

                if event.key == pygame.K_g:
                    algorithm = "gbfs"
                    current_path = gbfs(grid, agent_pos, goal) or []

    pygame.quit()

if __name__ == "__main__":
    main()