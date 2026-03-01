import pygame
import heapq

pygame.init()

# ================= USER GRID INPUT =================
ROWS = int(input("Enter number of rows: "))
COLS = int(input("Enter number of columns: "))

WIDTH = 1100
HEIGHT = 750
GRID_AREA = 750
CELL_SIZE = GRID_AREA // max(ROWS, COLS)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding - A* & GBFS")

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)

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
    while current in came_from:
        current = came_from[current]
        current.make_path()

# ================= A* =================
def astar(grid, start, goal):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))

    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start, goal)

    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal)
            return True

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, goal)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return False

# ================= GBFS =================
def gbfs(grid, start, goal):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))

    came_from = {}
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)[2]

        if current == goal:
            reconstruct_path(came_from, goal)
            return True

        visited.add(current)

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                count += 1
                heapq.heappush(open_set, (priority, count, neighbor))

    return False

# ================= GRID FUNCTIONS =================
def create_grid():
    return [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

def draw_grid(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    pygame.display.update()

def clear_path(grid):
    for row in grid:
        for node in row:
            if not node.is_obstacle and not node.is_start and not node.is_goal:
                node.color = WHITE

# ================= MAIN =================
def main():
    grid = create_grid()
    start = grid[0][0]
    goal = grid[ROWS-1][COLS-1]
    start.make_start()
    goal.make_goal()

    run = True
    while run:
        draw_grid(grid)

        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < GRID_AREA and y < GRID_AREA:
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    node = grid[row][col]
                    if event.button == 1:
                        node.make_obstacle()
                    elif event.button == 3:
                        node.remove_obstacle()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    clear_path(grid)
                    astar(grid, start, goal)

                if event.key == pygame.K_g:
                    clear_path(grid)
                    gbfs(grid, start, goal)

                if event.key == pygame.K_c:
                    clear_path(grid)

    pygame.quit()

if __name__ == "__main__":
    main()