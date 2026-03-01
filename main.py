import pygame

pygame.init()

# ================= USER GRID INPUT =================
ROWS = int(input("Enter number of rows: "))
COLS = int(input("Enter number of columns: "))

WIDTH = 1100
HEIGHT = 750
GRID_AREA = 750
CELL_SIZE = GRID_AREA // max(ROWS, COLS)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Grid")

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

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

# ================= GRID FUNCTIONS =================
def create_grid():
    return [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]

def draw_grid(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    # Draw grid lines
    for r in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, r * CELL_SIZE), (GRID_AREA, r * CELL_SIZE))
    for c in range(COLS):
        pygame.draw.line(WIN, GREY, (c * CELL_SIZE, 0), (c * CELL_SIZE, GRID_AREA))
    pygame.display.update()

# ================= MAIN PROGRAM =================
def main():
    grid = create_grid()
    start = grid[0][0]
    goal = grid[ROWS-1][COLS-1]
    start.make_start()
    goal.make_goal()

    run = True
    while run:
        draw_grid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x < GRID_AREA and y < GRID_AREA:
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    node = grid[row][col]
                    if event.button == 1:  # Left click - add obstacle
                        node.make_obstacle()
                    elif event.button == 3:  # Right click - remove obstacle
                        node.remove_obstacle()

    pygame.quit()

if __name__ == "__main__":
    main()