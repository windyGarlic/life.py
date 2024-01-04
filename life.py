import pygame
import sys
import random

# Constants
GRID_SIZE = 32
CELL_SIZE = 20
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CMA = [300, 320, 340, 360, 380, 400]
CREATURE_MAX_AGE = random.choice(CMA)
HUNGER_DECREASE_PER_TURN = 1
a = 0 

pygame.init()

DAY_DURATION = 5
day_counter = 0

# Font setup
font = pygame.font.Font(None, 24)

def display_day_counter():
    text_day = font.render(f"Days: {day_counter}", True, (0, 0, 0))
    text_plants = font.render(f"Plants: {count_entities('plant')}", True, (0, 0, 0))
    text_creatures = font.render(f"Creatures: {count_entities('creature')}", True, (0, 0, 0))
    
    screen.blit(text_day, (10, 10))
    screen.blit(text_plants, (10, 50))
    screen.blit(text_creatures, (10, 90))


def count_entities(entity_type):
    count = sum(1 for row in grid for cell in row if cell[0] == entity_type)
    return count

# Create the grid
grid = [[('empty', 0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Simulation")

def spawn_creatures():
    for _ in range(1):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[row][col][0] != 'empty':
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[row][col] = ('creature', {'age': 0, 'hunger': 100})

def move_creatures():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col][0] == 'creature':
                # Check for walls in a 1-tile radius
                near_wall = False
                for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
                    for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                        if grid[i][j][0] == 'wall':
                            near_wall = True
                            break

                if near_wall:
                    # Move creature away from the wall for the next 5 turns
                    if grid[row][col][1]['avoid_wall'] < 5:
                        # Find the wall direction
                        wall_direction = ''
                        if row == 0:
                            wall_direction = 'down'
                        elif row == GRID_SIZE - 1:
                            wall_direction = 'up'
                        elif col == 0:
                            wall_direction = 'right'
                        elif col == GRID_SIZE - 1:
                            wall_direction = 'left'

                        # Move creature away from the wall in the opposite direction
                        if wall_direction == 'up':
                            move_row, move_col = -1, 0
                        elif wall_direction == 'down':
                            move_row, move_col = 1, 0
                        elif wall_direction == 'left':
                            move_row, move_col = 0, -1
                        elif wall_direction == 'right':
                            move_row, move_col = 0, 1

                        # Increment the counter for turns to avoid the wall
                        grid[row][col][1]['avoid_wall'] += 1
                    else:

                        # Reset the counter and move randomly or towards the radius around the middle
                        move_row, move_col = move_towards_radius(row, col, radius=5)
                        grid[row][col] = ('creature', {'age': grid[row][col][1]['age'] + 1, 'hunger': grid[row][col][1]['hunger'], 'avoid_wall': 0})
                else:

                    # Move randomly or towards the radius around the middle
                    move_row, move_col = move_towards_radius(row, col, radius=5)

                new_row, new_col = row + move_row, col + move_col
                if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and grid[new_row][new_col][0] == 'empty':
                    grid[new_row][new_col] = ('creature', {'age': grid[row][col][1]['age'] + 1, 'hunger': grid[row][col][1]['hunger'], 'avoid_wall': 0})
                    grid[row][col] = ('empty', 0)

def move_towards_radius(row, col, radius):
    middle_row, middle_col = GRID_SIZE // 2, GRID_SIZE // 2
    distance_to_middle = max(abs(row - middle_row), abs(col - middle_col))

    
    move_row = random.choice([-1, 0, 1])
    move_col = random.choice([-1, 0, 1])

    return move_row, move_col

def creature_interaction():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col][0] == 'creature':

                food_distances = []
                food_positions = []

                # Check for food (plants or seeds) in a 2-tile radius
                for i in range(max(0, row - 2), min(GRID_SIZE, row + 3)):
                    for j in range(max(0, col - 2), min(GRID_SIZE, col + 3)):
                        if grid[i][j][0] == 'plant':

                            # Calculate Euclidean distance to the food
                            distance = ((i - row) ** 2 + (j - col) ** 2) ** 0.5
                            food_distances.append(distance)
                            food_positions.append((i, j))

                # Check if there are any food sources
                if food_distances:

                    # Find the position of the nearest food source
                    nearest_food_index = food_distances.index(min(food_distances))
                    nearest_food_position = food_positions[nearest_food_index]

                    # Move creature one tile closer to the nearest food
                    move_row = 1 if nearest_food_position[0] > row else -1 if nearest_food_position[0] < row else 0
                    move_col = 1 if nearest_food_position[1] > col else -1 if nearest_food_position[1] < col else 0

                    new_row, new_col = row + move_row, col + move_col
                    if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and grid[new_row][new_col][0] == 'empty':
                        grid[new_row][new_col] = ('creature', {'age': grid[row][col][1]['age'] + 1, 'hunger': grid[row][col][1]['hunger']})
                        grid[row][col] = ('empty', 0)

                    elif 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and (grid[new_row][new_col][0] == 'plant'):

                        # Eat the food and replace its position
                        grid[new_row][new_col] = ('creature', {'age': grid[row][col][1]['age'] + 1, 'hunger': grid[row][col][1]['hunger']})
                        grid[row][col] = ('empty', 0)

                        # Increase hunger by 10 when food is eaten
                        grid[new_row][new_col][1]['hunger'] = min(grid[new_row][new_col][1]['hunger'] + 10, 100)
                        return  # Only eat one food source per turn


def spawn_plants():
    for _ in range(12):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        while grid[row][col][0] != 'empty':
            row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        grid[row][col] = ('plant', 0)

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            #pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

            # Check for the tuple ('plant', age)
            if grid[row][col][0] == 'plant':
                age = grid[row][col][1]
                color = GREEN
                pygame.draw.circle(screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

            elif grid[row][col][0] == 'seed':  
                pygame.draw.circle(screen, YELLOW, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

            elif grid[row][col][0] == 'creature':  
                age = grid[row][col][1]['age']
                hunger = grid[row][col][1]['hunger']
                color = RED

                # Draw creature rectangle
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # Display age and hunger text
                font_size = 20  # Adjust the font size as needed
                font = pygame.font.Font(None, font_size)
                age_text = font.render(f"Age: {int(age/4)}", True, (0, 0, 0))
                hunger_text = font.render(f"Food: {hunger}", True, (0, 0, 0))

                # Position the text below the creature
                text_x = col * CELL_SIZE + CELL_SIZE // 2 - font_size
                text_y = row * CELL_SIZE + CELL_SIZE

                screen.blit(age_text, (text_x, text_y))
                screen.blit(hunger_text, (text_x, text_y + font_size + 2))


def simulate_life():
    global a
    if a < 1:
        spawn_plants()
        a += 1
    start_time = pygame.time.get_ticks()
    move_creatures()

    creature_interaction()
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col][0] == 'creature':
                # Age the creature and increase hunger
                age = grid[row][col][1]['age'] + 1
                hunger = grid[row][col][1]['hunger'] - HUNGER_DECREASE_PER_TURN  # Decrease hunger over time
                grid[row][col] = ('creature', {'age': age, 'hunger': max(0, hunger), 'avoid_wall': 0})

                # Check for lifespan condition
                if age >= CREATURE_MAX_AGE:
                    grid[row][col] = ('empty', 0)  # Creature dies
                elif hunger <= 0:
                    grid[row][col] = ('empty', 0)  # Creature dies

                # Reproduction when hunger reaches 100
                elif hunger > 80 and age >= 10:
                    spawn_reproduced_creature(row, col)
                    # Decrease hunger after reproduction to 40
                    grid[row][col][1]['hunger'] -= 60  # Adjust the value as needed

            elif grid[row][col][0] == 'plant':
                # Age the plant every 5 seconds
                current_time = pygame.time.get_ticks()
                if (current_time - start_time) // 1000 % 5 == 0:
                    age = grid[row][col][1] + 1
                    grid[row][col] = ('plant', age)

                    if age >= random.randint(20, 30):
                        grid[row][col] = ('empty', 0)
                    else:
                        if age % 5 == 0 and age <= 10:
                            seed_row, seed_col = row + random.randint(-1, 1), col + random.randint(-1, 1)

                            if 0 <= seed_row < GRID_SIZE and 0 <= seed_col < GRID_SIZE and grid[seed_row][seed_col][0] == 'empty':
                                grid[seed_row][seed_col] = ('seed', 0)

            elif grid[row][col][0] == 'seed':
                age = grid[row][col][1] + 1  # Increment age
                grid[row][col] = ('seed', age)  # Update seed age

                if 9 <= age <= 12:  # Check if the seed age is between 9 and 12
                    grid[row][col] = ('plant', 0)  # Convert seed to plant

def spawn_reproduced_creature(row, col):
    
    # Spawn a new creature adjacent to the parent creature
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and grid[new_row][new_col][0] == 'empty':
                grid[new_row][new_col] = ('creature', {'age': 0, 'hunger': 60, 'avoid_wall': 0, 'reproduction_delay': 10})
                return  # Stop spawning once a valid position is found

# Main game loop
running = True

# Initial setup
spawn_plants()
spawn_creatures()

# Time tracking for day counter
turn_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simulation logic
    simulate_life()

    # Increment day counter every DAY_DURATION turns
    turn_count += 1
    if turn_count % DAY_DURATION == 0:
        day_counter += 1

    # Draw the grid and day counter
    screen.fill(WHITE)
    draw_grid()
    display_day_counter()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(2)
