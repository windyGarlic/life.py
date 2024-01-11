import pygame
import sys
import random
import tkinter as tk
from tkinter import Label
import hashlib

#   TO DO 
#   ------
# Implement DNA (kinda done)
# Implement more stats
# Add predators
# Add error handling  
# Have program auto close when last creature dies

dna_list = []

class Ant:
    age = 0
    energy = 100
    reproduction_ready = True
    can_produce = False
    temp = 2
    all_ants_positions = []
    reproduction_cooldown = 0
    
    def __init__(self, initial_x, initial_y, name, dna, parent_1, parent_2 ):
        self.x = initial_x
        self.y = initial_y
        self.previous_direction = None  # Track the previous movement direction
        self.energy = 100
        self.name = name
        self.dna = dna
        self.color = self.generate_color(dna)
        self.parent_1 = parent_1
        self.parent_2 = parent_2
        dna_list.append(dna)
        self.child_count = 0
        genes = ["A","B","C","D","E","F"]        

        # 7 in 300 Chance of mutation when born
        if random.randint(1,300) == 1:
            modified_dna = dna[:0] + random.choice(genes) + dna[-7:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-1] + random.choice(genes) + dna[6:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-2] + random.choice(genes) + dna[5:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-3] + random.choice(genes) + dna[4:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-4] + random.choice(genes) + dna[3:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-5] + random.choice(genes) + dna[2:]
            self.dna = modified_dna
        if random.randint(1,300) == 1:
            modified_dna = dna[:-6] + random.choice(genes) + dna[1:]
            self.dna = modified_dna

        # Set Stats based on DNA
        if dna[0] == 'A':
            self.reproduction_age = 0.5
        elif dna[0] == 'B':
            self.reproduction_age = 1
        elif dna[0] == 'C':
            self.reproduction_age = 1.5
        elif dna[0] == 'D':
            self.reproduction_age = 2
        elif dna[0] == 'E':
            self.reproduction_age = 2.5
        elif dna[0] == 'F':
            self.reproduction_age = 3

        if dna[1] == 'A':
            self.metabolism = 1
        elif dna[1] == 'B':
            self.metabolism = 1.5
        elif dna[1] == 'C':
            self.metabolism = 2
        elif dna[1] == 'D':
            self.metabolism = 2.5
        elif dna[1] == 'E':
          self.  metabolism = 3
        elif dna[1] == 'F':
          self.  metabolism = 4

        if dna[2] == 'A':
            self.energy_gain = 20
        if dna[2] == 'B':
            self.energy_gain = 17
        if dna[2] == 'C':
            self.energy_gain = 15
        if dna[2] == 'D':
            self.energy_gain = 12
        if dna[2] == 'E':
            self.energy_gain = 10
        if dna[2] == 'F':
            self.energy_gain = 5

        if dna[3] == 'A':
            self.field_of_view_range = 1
        if dna[3] == 'B':
            self.field_of_view_range = 1
        if dna[3] == 'C':
            self.field_of_view_range = 2
        if dna[3] == 'D':
            self.field_of_view_range = 3
        if dna[3] == 'E':
            self.field_of_view_range = 4
        if dna[3] == 'F':
            self.field_of_view_range = 5

        if dna[4] == 'A':
            self.field_of_view_range_reproduction = 22
        if dna[4] == 'B':
            self.field_of_view_range_reproduction = 20
        if dna[4] == 'C':
            self.field_of_view_range_reproduction = 17
        if dna[4] == 'D':
            self.field_of_view_range_reproduction = 15
        if dna[4] == 'E':
            self.field_of_view_range_reproduction = 12
        if dna[4] == 'F':
            self.field_of_view_range_reproduction = 5

        if dna[5] == 'A':
            self.reproduction_limit = 18
        if dna[5] == 'B':
            self.reproduction_limit = 15
        if dna[5] == 'C':
            self.reproduction_limit = 14
        if dna[5] == 'D':
            self.reproduction_limit = 12
        if dna[5] == 'E':
            self.reproduction_limit = 10
        if dna[5] == 'F':
            self.reproduction_limit = 5

        if dna[6] == 'A':
            self.age_limit = 15
        if dna[6] == 'B':
            self.age_limit = 14
        if dna[6] == 'C':
            self.age_limit = 13
        if dna[6] == 'D':
            self.age_limit = 12
        if dna[6] == 'E':
            self.age_limit = 11
        if dna[6] == 'F':
            self.age_limit = 7

    def move(self, direction):
        pygame.draw.circle(screen, (0, 0, 0), (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2 - 5)

        if direction == "UP" and self.y > 0:
            self.y -= 1
        elif direction == "DOWN" and self.y < GRID_SIZE - 1:
            self.y += 1
        elif direction == "LEFT" and self.x > 0:
            self.x -= 1
        elif direction == "RIGHT" and self.x < GRID_SIZE - 1:
            self.x += 1

        self.draw()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 2 - 5)
    
    def getDirection(self):
        global food_position
        global ants

        options = ["UP", "DOWN", "LEFT", "RIGHT"]
        candidate_directions = []

# Move to food
        for direction in options:
           for i in range(1, self.field_of_view_range + 1):
               new_x, new_y = self.x, self.y

               if direction == "UP":
                   new_y -= i
               elif direction == "DOWN":
                   new_y += i
               elif direction == "LEFT":
                   new_x -= i
               elif direction == "RIGHT":
                   new_x += i

               if (new_x, new_y) in food_position:
                   candidate_directions.append(direction)
       
        if candidate_directions:
           # If there are candidate directions, choose one randomly
           direction = random.choice(candidate_directions)
           new_x, new_y = self.x, self.y

           if direction == "UP":
               new_y -= 1
           elif direction == "DOWN":
               new_y += 1
           elif direction == "LEFT":
               new_x -= 1
           elif direction == "RIGHT":
               new_x += 1

           if (new_x, new_y) in food_position:
               food_position.remove((new_x, new_y))
               print(f"Food consumed at position ({new_x}, {new_y})")
               self.energy += self.energy_gain
               return direction
           else:
               direction = random.choice(options)

        # Move to other ant
        if self.reproduction_ready == True:
            for direction in options:
                for i in range(1, self.field_of_view_range_reproduction + 1):
                   new_x, new_y = self.x, self.y

                   if direction == "UP":
                       new_y -= i
                   elif direction == "DOWN":
                       new_y += i
                   elif direction == "LEFT":
                       new_x -= i
                   elif direction == "RIGHT":
                       new_x += i
                   candidate_directions = []
                   if (new_x, new_y) in Ant.all_ants_positions:
                       candidate_directions.append(direction)

        if candidate_directions:
           # If there are candidate directions, choose one randomly
           direction = random.choice(candidate_directions)
           new_x, new_y = self.x, self.y

           if direction == "UP":
               new_y -= 1
           elif direction == "DOWN":
               new_y += 1
           elif direction == "LEFT":
               new_x -= 1
           elif direction == "RIGHT":
               new_x += 1

           if (new_x, new_y) in food_position:
               food_position.remove((new_x, new_y))
               print(f"Food consumed at position ({new_x}, {new_y})")
               self.energy += self.energy_gain
                    
        else:
           direction = random.choice(options)

        return direction

    def consumeFood(self, direction):
        global food_position

        # Calculate the new position after moving in the specified direction
        new_x, new_y = self.x, self.y

        if direction == "UP":
            new_y -= 1
        elif direction == "DOWN":
            new_y += 1
        elif direction == "LEFT":
            new_x -= 1
        elif direction == "RIGHT":
            new_x += 1

        # Check if the new position has food
        if (new_x, new_y) in food_position:
            # Remove the consumed food from the list
            food_position.remove((new_x, new_y))
            print(f"Food consumed at position ({new_x}, {new_y})")
            self.energy += self.energy_gain

        # Move the ant in the specified direction
        self.move(direction)

    def die(self):
        print(f"Ant at position ({self.x}, {self.y}) has died.")
        ants.remove(self)
    
    def generate_color(self, gene):
        hashed = hashlib.sha256(gene.encode()).hexdigest()

        # Extract three segments of 8 characters each and convert to decimal
        r = int(hashed[:8], 16) % 256
        g = int(hashed[8:16], 16) % 256
        b = int(hashed[16:24], 16) % 256

        return (r, g, b)

     
class Food:
    def __init__(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y

    def draw(self):
        screen.blit(FOOD_ICON, (self.x * CELL_SIZE - 22.5 , self.y * CELL_SIZE - 22.5))

    def drop_seed(self):
        global food_position

        # Generate positions for seeds in a 1-tile radius
        seed_positions = [
            (self.x, self.y - 2),
            (self.x, self.y + 2),
            (self.x - 2, self.y),
            (self.x + 2, self.y) ]

        for seed_pos in seed_positions:
            if seed_pos not in food_position:
                x, y = seed_pos
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    food_position.append(seed_pos)

    def draw_seed(self, seed_pos):
        pygame.draw.circle(screen, (255, 255, 0), (seed_pos[0] * CELL_SIZE + CELL_SIZE // 2, seed_pos[1] * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 4)


def is_click_inside_any_ant(click_pos, ants):
    for ant in ants:
        ant_rect = pygame.Rect(ant.x * CELL_SIZE, ant.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if ant_rect.collidepoint(click_pos):
            return ant
    return None

def display_ant_stats_tkinter(selected_ant):
    if selected_ant is not None:
        stats_window = tk.Tk()
        stats_window.title(f"{selected_ant} Stats")
                
        ant_position_label = Label(stats_window, text=f"Name: ({selected_ant.name})")
        ant_position_label.pack()
        
        ant_position_label = Label(stats_window, text=f"Parents: ({selected_ant.parent_1}, {selected_ant.parent_2})")
        ant_position_label.pack()

        ant_position_label = Label(stats_window, text=f"Position: ({selected_ant.x}, {selected_ant.y})")
        ant_position_label.pack()
        updated_age = round(selected_ant.age, 2)
        ant_age_label = Label(stats_window, text=f"Age: {updated_age}")
        ant_age_label.pack()
        ant_dna_label = Label(stats_window, text=f"DNA: {selected_ant.dna}")
        ant_dna_label.pack()
        ant_energy_label = Label(stats_window, text=f"Energy: {selected_ant.energy} ")
        ant_energy_label.pack()

        ant_energy_label = Label(stats_window, text=f"Age till sterile: {selected_ant.reproduction_limit} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Start reproducing age: {selected_ant.reproduction_age} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Metabolism: {selected_ant.metabolism} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Energy Gain: {selected_ant.energy_gain} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Food detection range: {selected_ant.field_of_view_range} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Mate detection range: {selected_ant.field_of_view_range_reproduction} ")
        ant_energy_label.pack()
        ant_energy_label = Label(stats_window, text=f"Number of children: {selected_ant.child_count} ")
        ant_energy_label.pack()
        

        def check_pygame_events():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            stats_window.after(10, check_pygame_events)

        check_pygam
e_events()
        stats_window.mainloop()

def list_has_neighbors(lst, threshold=1):
    seen = {}
    for i, value in enumerate(lst):
        for j, existing_value in seen.items():
            if isinstance(value, tuple) and isinstance(existing_value, tuple):
                if all(abs(v1 - v2) <= threshold for v1, v2 in zip(value, existing_value)):
                    return True, j, i
        seen[i] = value
    return False, None, None

# Constants
GRID_SIZE = 14
CELL_SIZE = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FOOD_ICON = pygame.image.load('food_icon.png')

# Game variables
turn_counter = 0
ant  = Ant(10, 10, "dave",  "ABCDEFA", "NA", "NA")
ant2 = Ant(10, 10, "mel",   "BCDEFAB", "NA", "NA")
ant3 = Ant(10, 10, "frank", "CDEFABC", "NA", "NA")
ant4 = Ant(10, 10, "jill",  "DEFABCD", "NA", "NA")
ant5 = Ant(10, 10, "paul",  "EFABCDE", "NA", "NA")
ant6 = Ant(10, 10, "gomez", "FABCDEF", "NA", "NA")

new_ant = ''
food_position = []
num_child_count = []
ants = [ant, ant2, ant3, ant4, ant5, ant6]

#spawn initial food
food1 = Food(4, 6)
food2 = Food(8, 8)
food3 = Food(13,3)
food4 = Food(14,14)
food5 = Food(9, 12)
food6 = Food(4, 7)
food7 = Food(13, 5)
food8 = Food(2, 3)
food9 = Food(3, 16)

food1Pos = food1.x, food1.y
food2Pos = food2.x, food2.y
food3Pos = food3.x, food3.y
food4Pos = food4.x, food4.y
food5Pos = food5.x, food5.y
food6Pos = food6.x, food6.y
food7Pos = food7.x, food7.y
food8Pos = food8.x, food8.y
food9Pos = food9.x, food9.y

food_position.append(food1Pos)
food_position.append(food2Pos)
food_position.append(food3Pos)
food_position.append(food4Pos)
food_position.append(food5Pos)
food_position.append(food6Pos)
food_position.append(food7Pos)
food_position.append(food8Pos)
food_position.append(food9Pos)

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Life")

# Game loop
running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any ant is clicked
            clicked_ant = is_click_inside_any_ant(pygame.mouse.get_pos(), ants)
            if clicked_ant is not None:
                display_ant_stats_tkinter(clicked_ant)

    if not paused:
 
        screen.fill((0, 0, 0))

        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, GRID_SIZE * CELL_SIZE))
        for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (GRID_SIZE * CELL_SIZE, y))

        # Each turn
        if turn_counter % 1 == 0:

            # Draw food based on the food_position list
            for food_pos in food_position:
                food = Food(food_pos[0], food_pos[1])
                food.draw()
            print(f"\nPlant_pos: {food_position}")

            ant_counter = 1
            has_neighbors, parent_1, parent_2 = list_has_neighbors(Ant.all_ants_positions)

            for i in ants:
                # Reproduction
                try:
                    if i.age > i.reproduction_age and i.reproduction_ready and i == parent_1_object and i.reproduction_cooldown == 0:
                        i.can_produce = True
                    else:
                        i.can_produce = False
                except:
                    pass

            if has_neighbors:
                parent_1_object = ants[int(parent_1)]
                parent_2_object = ants[int(parent_2)]
                
                for i in ants:
                    if i.parent_1 == parent_1_object or parent_2_object:
                        i.can_produce == False
                    if parent_2 == parent_1_object or parent_2_object:
                        i.can_produce == False

                dna = ''
                dna1 = [parent_1_object.dna[0], parent_2_object.dna[0]]
                dna += random.choice(dna1)

                dna2 = [parent_1_object.dna[1], parent_2_object.dna[1]]
                dna += random.choice(dna2)

                dna3 = [parent_1_object.dna[2], parent_2_object.dna[2]]
                dna += random.choice(dna3)
                
                dna4 = [parent_1_object.dna[3], parent_2_object.dna[3]]
                dna += random.choice(dna4)

                dna5 = [parent_1_object.dna[4], parent_2_object.dna[4]]
                dna += random.choice(dna5)

                dna6 = [parent_1_object.dna[5], parent_2_object.dna[5]]
                dna += random.choice(dna6)

                dna7 = [parent_1_object.dna[6], parent_2_object.dna[6]]
                dna += random.choice(dna7)

                if has_neighbors:
                    if parent_1_object.can_produce:
                        # Generate a unique variable name
                        new_ant_var_name = f"new_ant_{ant_counter}"
                        globals()[new_ant_var_name] = Ant(parent_1_object.x, parent_2_object.y, random.randint(0,200), dna, parent_1_object.name, parent_2_object.name)
                        ants.append(globals()[new_ant_var_name])
                        ant_counter += 1
                        parent_1_object.energy -= 50
                        parent_1_object.child_count += 1
                        parent_2_object.child_count += 1

    
                        print(f"{new_ant_var_name} spawned!")
                        Ant.temp += 1
                        parent_1_object.reproduction_cooldown = 1
                        parent_2_object.reproduction_cooldown = 1
    
                        print (parent_1_object.name)
                        print (parent_1_object.dna)
                        print (parent_2_object.name)
                        print (parent_2_object.dna)
                        has_neighbors = False
    
            x = 0
            Ant.all_ants_positions = []
            
            for i in ants:
                if i.energy <= 0 or i.age > i.age_limit:
                    i.die()
                    num_child_count.append(i.child_count)
                i.move(ant.getDirection())
                
                ant_position = i.x, i.y
                Ant.all_ants_positions.append(ant_position)
                i.age += 0.1
                i.energy -= i.metabolism
                i.consumeFood(i.getDirection())
                print(f"{i.name} energy: {i.energy}")
                print(f"{i.name} pos: {ant_position}")
                print(Ant.all_ants_positions)
                x += 1

        if turn_counter % 10 == 0:
            food.drop_seed()
            food2.drop_seed()
            food1.drop_seed()
            food3.drop_seed()
            food4.drop_seed()
            food5.drop_seed()
            food6.drop_seed()
            food7.drop_seed()
            food8.drop_seed()
            food9.drop_seed()
            
        
        if turn_counter % 25 == 0:
            for i in ants:
                i.reproduction_cooldown = 0
        turn_counter += 1
        has_neighbors = False

        print(dna_list)
        pygame.display.flip()
        pygame.time.delay(10)

pygame.quit()
