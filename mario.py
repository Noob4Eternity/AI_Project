import pygame
import heapq

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 500, 500
TILE_SIZE = 100
ROWS, COLS = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Mario Pathfinding")

# Node class
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

# A* algorithm
def astar(grid, start, goal):
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start)

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.add((current_node.x, current_node.y))

        if current_node.x == goal.x and current_node.y == goal.y:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_x, neighbor_y = current_node.x + dx, current_node.y + dy

            if not (0 <= neighbor_x < ROWS) or not (0 <= neighbor_y < COLS) or grid[neighbor_x][neighbor_y] == 1:
                continue

            neighbor = Node(neighbor_x, neighbor_y, current_node)

            if (neighbor.x, neighbor.y) in closed_list:
                continue

            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h

            heapq.heappush(open_list, neighbor)

    return None

# Draw grid and path
def draw_grid(grid, path):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 0)

    for (x, y) in path:
        pygame.draw.rect(screen, GREEN, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Main game loop
def main():
    clock = pygame.time.Clock()

    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]

    start = Node(0, 0)
    goal = Node(4, 4)

    path = astar(grid, start, goal)

    running = True
    while running:
        screen.fill(BLUE)

        draw_grid(grid, path)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
