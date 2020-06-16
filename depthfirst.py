"""
Generate a maze using the Depth-first search algorithm
https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""
import random
import pygame

from maze import Maze


def paint_wall(x, y, direction, color=(0, 0, 255, 15)):
    """Painting the wall between cells with a given color

    Args:
        x (int): cell horizontal coordinate
        y (int): cell vertical coordinate
        direction (str): navigation direction (N,S,E,W)
        color (tuple): an (RGB) triplet

    """
    dx = x * cell_width
    dy = y * cell_height

    if direction == 'N':
        line_head = (dx + 1, dy)
        line_tail = (dx + cell_width - 1, dy)
    elif direction == 'S':
        line_head = (dx + 1, dy + cell_width)
        line_tail = (dx + cell_width - 1, dy + cell_height)
    elif direction == 'E':
        line_head = (dx + cell_width, dy + 1)
        line_tail = (dx + cell_width, dy + cell_height - 1)
    elif direction == 'W':
        line_head = (dx, dy + 1)
        line_tail = (dx, dy + cell_height - 1)

    pygame.draw.line(game_surface, color, line_head, line_tail)


def draw_cell(x, y, color=(255, 255, 0)):
    """Drawing the cell with a given color

    Args:
        x (int): cell horizontal coordinate
        y (int): cell vertical coordinate
        color (tuple): an (RGB) triplet

    """
    x0 = int(x * cell_width + 1)
    y0 = int(y * cell_height + 1)
    w0 = int(cell_width - 1)
    h0 = int(cell_height - 1)

    pygame.draw.rect(game_surface, color, (x0, y0, w0, h0))


if __name__ == '__main__':
    # Initialize game
    pygame.init()
    pygame.display.set_caption("Maze generator - Depth-first search algorithm")

    # Defining display screen size
    screen_width, screen_height = 500, 500
    screen = pygame.display.set_mode((screen_width + 1, screen_height + 1))

    # Colors palette
    PRIMARY_COLOR = (61, 1, 84)
    SECONDARY_COLOR = (253, 231, 36)

    # Defining maze attributes
    nx, ny = 10, 10

    # Creating a new maze
    maze = Maze(nx, ny)

    # Calculating cell size
    cell_width = screen_width // nx
    cell_height = screen_height // ny

    # Creating background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill(PRIMARY_COLOR)

    # Creating the game layer
    game_surface = pygame.Surface(screen.get_size()).convert_alpha()
    game_surface.fill((0, 0, 0, 0,))

    # Drawing horizontal lines
    for y in range(ny + 1):
        pygame.draw.line(game_surface, PRIMARY_COLOR, (0, y * cell_height), (screen_width, y * cell_height))

    # Drawing vertical lines
    for x in range(nx + 1):
        pygame.draw.line(game_surface, PRIMARY_COLOR, (x * cell_width, 0), (x * cell_width, screen_height))

    # Choose initial cell, mark it as visited and push it to the stack
    current_cell = maze.cell_at(random.randint(0, maze.nx - 1), random.randint(0, maze.ny - 1))
    cell_stack = [current_cell]

    while True:
        ms = 0
        # If the stack is not empty
        if cell_stack:
            # Pop a cell from the stack and make it a current cell
            current_cell = cell_stack.pop()
            unvisited_neighbours = maze.find_valid_neighbours(current_cell)
            draw_cell(current_cell.x, current_cell.y, SECONDARY_COLOR)

            # If the current cell has any neighbours which have not been visited
            if unvisited_neighbours:
                # Push the current cell to the stack
                cell_stack.append(current_cell)
                # Choose one of the unvisited neighbours
                wall_direction, next_cell = random.choice(unvisited_neighbours)
                # Remove the wall between the current cell and the chosen cell
                current_cell.break_wall(next_cell, wall_direction)
                paint_wall(current_cell.x, current_cell.y, wall_direction, SECONDARY_COLOR)
                # Mark the chosen cell as visited and push it to the stack
                cell_stack.append(next_cell)
                ms = 50

        # Updating screen
        screen.blit(background, (0, 0))
        screen.blit(game_surface, (0, 0))

        # Rendering
        pygame.display.flip()

        # Handling any incoming event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # Changing FPS (frames per second)
        pygame.time.wait(ms)
