import pygame
import math
import random
from queue import PriorityQueue

pygame.init()

# ================= USER GRID INPUT =================
ROWS = int(input("Enter number of rows: "))
COLS = int(input("Enter number of columns: "))

VISUALIZATION_DELAY = 20

WIDTH = 1100
HEIGHT = 650
GRID_AREA = 650
CELL_SIZE = GRID_AREA // max(ROWS, COLS)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")

FONT = pygame.font.SysFont("Arial", 18)

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
DARK_GREY = (50, 50, 50)

# ================= BUTTON =================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.active = False

    def draw(self):
        color = CYAN if self.active else DARK_GREY
        pygame.draw.rect(WIN, color, self.rect)
        pygame.draw.rect(WIN, BLACK, self.rect, 2)
        txt = FONT.render(self.text, True, WHITE)
        text_rect = txt.get_rect(center=self.rect.center)
        WIN.blit(txt, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ================= NODE =================
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.parent = None
        self.is_start = False
        self.is_goal = False
        self.is_obstacle = False
        self.is_visited = False
        self.is_frontier = False
        self.is_path = False
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

    def draw(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(WIN, GREY, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)

    def make_start(self):
        self.is_start = True
        self.color = GREEN
        self.is_obstacle = False

    def make_goal(self):
        self.is_goal = True
        self.color = BLUE
        self.is_obstacle = False

    def make_obstacle(self):
        if not self.is_start and not self.is_goal:
            self.is_obstacle = True
            self.color = BROWN

    def remove_obstacle(self):
        if not self.is_start and not self.is_goal:
            self.is_obstacle = False
            self.color = WHITE

    def make_frontier(self):
        if not self.is_start and not self.is_goal:
            self.is_frontier = True
            self.color = YELLOW

    def make_visited(self):
        if not self.is_start and not self.is_goal:
            self.is_visited = True
            self.color = RED

    def make_path(self):
        if not self.is_start and not self.is_goal:
            self.is_path = True
            self.color = PURPLE

    def reset_search(self):
        if not self.is_start and not self.is_goal and not self.is_obstacle:
            self.color = WHITE
        self.is_visited = False
        self.is_frontier = False
        self.is_path = False
        self.parent = None
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbor = grid[r][c]
                if not neighbor.is_obstacle:
                    self.neighbors.append(neighbor)

# ================= HEURISTICS =================
def manhattan(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def euclidean(a, b):
    return math.sqrt((a.row - b.row)**2 + (a.col - b.col)**2)

# ================= GRID =================
def create_grid():
    return [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

def draw_grid():
    for r in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, r*CELL_SIZE), (GRID_AREA, r*CELL_SIZE))
    for c in range(COLS):
        pygame.draw.line(WIN, GREY, (c*CELL_SIZE, 0), (c*CELL_SIZE, GRID_AREA))

def clear_search(grid):
    for row in grid:
        for node in row:
            node.reset_search()

def clear_all_obstacles(grid, start, goal):
    for row in grid:
        for node in row:
            if node != start and node != goal:
                node.remove_obstacle()

def random_obstacles(grid, density, start, goal):
    for row in grid:
        for node in row:
            if node != start and node != goal and random.random() < density:
                node.make_obstacle()

def spawn_dynamic_obstacle(grid, start, goal):
    for _ in range(10):
        r = random.randint(0, ROWS-1)
        c = random.randint(0, COLS-1)
        node = grid[r][c]
        if node != start and node != goal and not node.is_obstacle:
            node.make_obstacle()
            return node
    return None

# ================= PATH RECONSTRUCTION =================
def reconstruct_path(goal):
    path = []
    cur = goal
    while cur.parent:
        path.append(cur)
        cur = cur.parent
    return path[::-1]

# ================= SEARCH ALGORITHMS =================
def astar(draw, grid, start, goal, heur):
    count = 0
    pq = PriorityQueue()
    start.g = 0
    start.h = heur(start, goal)
    start.f = start.g + start.h
    pq.put((start.f, count, start))
    open_set_hash = {start}

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        current = pq.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            path = reconstruct_path(goal)
            for node in path:
                node.make_path()  # Show full path instantly
            return path

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                neighbor.h = heur(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in open_set_hash:
                    count += 1
                    pq.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()

        if current != start:
            current.make_visited()

        draw()
        pygame.time.delay(VISUALIZATION_DELAY)

    return None

def gbfs(draw, grid, start, goal, heur):
    count = 0
    pq = PriorityQueue()
    start.h = heur(start, goal)
    pq.put((start.h, count, start))
    open_set_hash = {start}
    closed_set = set()

    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        current = pq.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            path = reconstruct_path(goal)
            for node in path:
                node.make_path()
            return path

        closed_set.add(current)

        for neighbor in current.neighbors:
            if neighbor not in closed_set and neighbor not in open_set_hash:
                neighbor.parent = current
                neighbor.h = heur(neighbor, goal)
                count += 1
                pq.put((neighbor.h, count, neighbor))
                open_set_hash.add(neighbor)
                neighbor.make_frontier()

        if current != start:
            current.make_visited()

        draw()
        pygame.time.delay(VISUALIZATION_DELAY)

    return None

# ================= DYNAMIC SEARCH =================
def dynamic_search(draw, grid, start, goal, algo, heur):
    current_pos = start
    while current_pos != goal:
        for row in grid:
            for node in row:
                node.update_neighbors(grid)

        if algo == "A*":
            path = astar(draw, grid, current_pos, goal, heur)
        else:
            path = gbfs(draw, grid, current_pos, goal, heur)

        if not path:
            return

        for step in path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if random.random() < 0.03:
                new_obstacle = spawn_dynamic_obstacle(grid, start, goal)
                if new_obstacle and new_obstacle in path[path.index(step):]:
                    clear_search(grid)
                    current_pos = step
                    current_pos.color = RED
                    draw()
                    break

            current_pos = step
            if current_pos == goal:
                return

# ================= DRAW FUNCTIONS =================
def draw_all(grid, buttons):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    draw_grid()
    pygame.draw.rect(WIN, GREY, (GRID_AREA, 0, WIDTH - GRID_AREA, HEIGHT))
    for b in buttons:
        b.draw()
    pygame.display.update()

# ================= MAIN PROGRAM =================
def main():
    grid = create_grid()
    start = grid[0][0]
    goal = grid[ROWS-1][COLS-1]
    start.make_start()
    goal.make_goal()

    panel_x = 800
    btn_width = 260
    btn_height = 40
    spacing = 8
    y_pos = 50

    btn_astar = Button(panel_x, y_pos, btn_width, btn_height, "Algorithm: A*")
    y_pos += btn_height + spacing
    btn_gbfs = Button(panel_x, y_pos, btn_width, btn_height, "Algorithm: GBFS")
    y_pos += btn_height + spacing * 2
    btn_manh = Button(panel_x, y_pos, btn_width, btn_height, "Heuristic: Manhattan")
    y_pos += btn_height + spacing
    btn_eucl = Button(panel_x, y_pos, btn_width, btn_height, "Heuristic: Euclidean")
    y_pos += btn_height + spacing * 2
    btn_set_start = Button(panel_x, y_pos, btn_width, btn_height, "Set Start (S)")
    y_pos += btn_height + spacing
    btn_set_goal = Button(panel_x, y_pos, btn_width, btn_height, "Set Goal (G)")
    y_pos += btn_height + spacing * 2
    btn_random = Button(panel_x, y_pos, btn_width, btn_height, "Random Map (30%)")
    y_pos += btn_height + spacing
    btn_clear_obs = Button(panel_x, y_pos, btn_width, btn_height, "Clear Obstacles")
    y_pos += btn_height + spacing * 2
    btn_start = Button(panel_x, y_pos, btn_width, btn_height, "START SEARCH")
    y_pos += btn_height + spacing
    btn_reset = Button(panel_x, y_pos, btn_width, btn_height, "Reset Grid")

    buttons = [btn_astar, btn_gbfs, btn_manh, btn_eucl, btn_set_start, btn_set_goal,
               btn_random, btn_clear_obs, btn_start, btn_reset]

    algo = "A*"
    heur = manhattan
    heur_name = "Manhattan"
    setting_mode = None
    btn_astar.active = True
    btn_manh.active = True

    run = True
    while run:
        draw_all(grid, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_astar.clicked(pos):
                    algo = "A*"
                    btn_astar.active = True
                    btn_gbfs.active = False
                elif btn_gbfs.clicked(pos):
                    algo = "GBFS"
                    btn_gbfs.active = True
                    btn_astar.active = False
                elif btn_manh.clicked(pos):
                    heur = manhattan
                    heur_name = "Manhattan"
                    btn_manh.active = True
                    btn_eucl.active = False
                elif btn_eucl.clicked(pos):
                    heur = euclidean
                    heur_name = "Euclidean"
                    btn_eucl.active = True
                    btn_manh.active = False
                elif btn_set_start.clicked(pos):
                    setting_mode = 'start' if setting_mode != 'start' else None
                elif btn_set_goal.clicked(pos):
                    setting_mode = 'goal' if setting_mode != 'goal' else None
                elif btn_random.clicked(pos):
                    clear_search(grid)
                    random_obstacles(grid, 0.3, start, goal)
                elif btn_clear_obs.clicked(pos):
                    clear_all_obstacles(grid, start, goal)
                elif btn_reset.clicked(pos):
                    grid = create_grid()
                    start = grid[0][0]
                    goal = grid[ROWS-1][COLS-1]
                    start.make_start()
                    goal.make_goal()
                elif btn_start.clicked(pos):
                    clear_search(grid)
                    dynamic_search(lambda: draw_all(grid, buttons), grid, start, goal, algo, heur)

                # Grid clicks
                if event.button == 1:  # left click
                    x, y = pos
                    if x < GRID_AREA and y < GRID_AREA:
                        node = grid[y // CELL_SIZE][x // CELL_SIZE]
                        if setting_mode == 'start' and node != goal:
                            start.is_start = False
                            start.color = WHITE
                            start = node
                            start.make_start()
                            setting_mode = None
                        elif setting_mode == 'goal' and node != start:
                            goal.is_goal = False
                            goal.color = WHITE
                            goal = node
                            goal.make_goal()
                            setting_mode = None
                        elif node != start and node != goal:
                            if node.is_obstacle:
                                node.remove_obstacle()
                            else:
                                node.make_obstacle()
                elif event.button == 3:  # right click
                    x, y = pos
                    if x < GRID_AREA and y < GRID_AREA:
                        node = grid[y // CELL_SIZE][x // CELL_SIZE]
                        if node != start and node != goal:
                            node.remove_obstacle()
    pygame.quit()

if __name__ == "__main__":
    main()