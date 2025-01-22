import tkinter as tk
from collections import deque
import random
# Constants for default grid size
DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10

# Directions for movement in the maze (up, down, left, right)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Maze state
START = 'S'
GOAL = 'G'
OBSTACLE = 'O'
EMPTY = 'E'

class MicromouseMaze:
    def __init__(self,root):
        self.root = root
        self.grid_width = DEFAULT_WIDTH
        self.grid_height = DEFAULT_HEIGHT
        self.grid = [[EMPTY for _ in range(self.grid_width)] for _ in range(self.grid_height)]   #make a list of grid
        self.start = None
        self.goal = None
        self.current_mode = EMPTY  # Initially no mode is selected (empty blocks)

        # Create the canvas to display maze
        self.canvas = tk.Canvas(root, width=self.grid_width * 50, height=self.grid_height * 50)
        self.canvas.place(x=50,y=50)
        self.canvas.bind("<Button-1>", self.on_click)

        # Buttons and options
        self.select_obstacle_button = tk.Button(root, text="Select Obstacle",command=self.select_obstacle)
        self.select_obstacle_button.place(x=520,y=60)
        self.select_start_button = tk.Button(root, text="Select Start",command=self.select_start)
        self.select_start_button.place(x=520,y=95)
        self.select_goal_button = tk.Button(root, text="Select Goal",command=self.select_goal)
        self.select_goal_button.place(x=520,y=130)
        self.solve_button = tk.Button(root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.place(x=520,y=165)
        self.random_obstacle_button = tk.Button(root, text="Random Obstacles",command=self.add_random_obstacles)
        self.random_obstacle_button.place(x=520,y=200)
        self.reset_button = tk.Button(root, text="Reset Maze", command=self.reset_maze)
        self.reset_button.place(x=520,y=240)

        # Grid size selection
        self.grid_width_label = tk.Label(root, text="Grid Width:")
        self.grid_width_label.place(x=520,y=280)
        self.grid_width_entry = tk.Entry(root)
        self.grid_width_entry.insert(0, str(self.grid_width))
        self.grid_width_entry.place(x=590,y=280)
        self.grid_height_label = tk.Label(root, text="Grid Height:")
        self.grid_height_label.place(x=520,y=310)
        self.grid_height_entry = tk.Entry(root)
        self.grid_height_entry.insert(0, str(self.grid_height))
        self.grid_height_entry.place(x=590,y=310)
        self.update_size_button = tk.Button(root, text="Update Grid Size",command=self.update_grid_size)
        self.update_size_button.place(x=520,y=340)

        # Draw the initial grid
        self.draw_grid()

    def select_obstacle(self):
        self.current_node = OBSTACLE  # Set node to obstacle
    def select_start(self):
        self.current_node = START  # Set node to start
    def select_goal(self):
        self.current_node = GOAL  # Set node to goal

    #Function for grid
    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                 color = "white"
                 if self.grid[i][j] == OBSTACLE:
                      color = "black"
                 elif self.grid[i][j] == START:
                      color = "green"
                 elif self.grid[i][j] == GOAL:
                      color = "red"
                 self.canvas.create_rectangle(j * 30, i *30,( j+ 1) * 30, (i + 1) * 30,fill=color, outline="black")
    def on_click(self, event):
        row = event.y // 30
        col = event.x // 30
        if self.current_node == OBSTACLE:
            self.grid[row][col] = OBSTACLE
        elif self.current_node == START:
            if self.start:  # If start already set, change it to empty
                self.grid[self.start[0]][self.start[1]] = EMPTY
            self.grid[row][col] = START
            self.start = (row, col)
        elif self.current_node == GOAL:
            if self.goal:  # If goal already set, change it to empty
                self.grid[self.goal[0]][self.goal[1]] = EMPTY
            self.grid[row][col] = GOAL
            self.goal = (row, col)
        # Redraw the grid with the updated states
        self.draw_grid()
        return self.start ,self.goal
    def reset_maze(self):
         self.start = None
         self.goal = None
         self.grid = [[EMPTY for _ in range(self.grid_width)] for _ in range(self.grid_height)]
         self.draw_grid()
    def update_grid_size(self):  # Get new grid size from entry fields
        try:
             self.grid_width = int(self.grid_width_entry.get())
             self.grid_height = int(self.grid_height_entry.get())
             # Resize the grid
             self.grid = [[EMPTY for _ in range(self.grid_width)] for _ in range(self.grid_height)]
             # Resize the canvas
             self.canvas.config(width=self.grid_width * 30, height=self.grid_height * 30)
             self.draw_grid()
             return self.grid_width,self.grid_height
        except ValueError:
             print("Invalid grid size values")
    def add_random_obstacles(self):  # Ask for the obstacle density (percentage)
         obstacle_density = 0.2  # Default 20% obstacles
         for i in range(self.grid_height):
             for j in range(self.grid_width):
                  if random.random() < obstacle_density:
                       self.grid[i][j] = OBSTACLE
                       self.draw_grid()
    def solve_maze(self):
         if not self.start or not self.goal:
              print("Start or goal not set!")
              return
         path = self.bfs(self.start, self.goal)

         if path:
              self.highlight_path(path)  #This will draw path
         else:
              print("No path found!")
    def bfs(self, start, goal):
         # Queue for BFS
         queue = deque([start])
         # Parent map to reconstruct the path
         parent_map = {start: None}
         # Set of visited cells
         visited = set()
         visited.add(start)
         while queue:
             current = queue.popleft()
             if current == goal: #Reconstruct the path by backtracking through parent_map
                 path = []
                 while current:
                     path.append(current)
                     current = parent_map[current]
                 path.reverse()
                 path.remove(start)
                 path.remove(goal)
                 return path
         # Check all 4 adjacent cells (up, down, left, right)
             for direction in DIRECTIONS:
                 neighbor = (current[0] + direction[0], current[1] + direction[1])
                 if 0 <= neighbor[0] < self.grid_height and 0 <= neighbor[1] <self.grid_width:
                     if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] !=OBSTACLE:
                             visited.add(neighbor)
                             parent_map[neighbor] = current
                             queue.append(neighbor)
         return None  # No path found
    def highlight_path(self, path):  # Highlight the path in blue
         for (r, c) in path:
             self.canvas.create_rectangle(c * 30, r * 30,( c+ 1) * 30, (r + 1) * 30,fill="yellow", outline="black")
# Create the Tkinter window
root = tk.Tk()
root.title("Micromouse Maze Solver")
maze = MicromouseMaze(root)
root.minsize(width=1000,height=1000)
label=tk.Label(text="Welcome to the Micromouse Maze Game")
label1=tk.Label(text="#Please use the given below button to play the game")
label1.place(x=520,y=35)
label.place(x=550,y=10)
label2=tk.Label(text="Note:If grid_width and grid_height is increased above 15,Maze come over buttons. Sorry for the inconvenience. Please co-operate.")
label2.place(x=100,y=600)
# Start the Tkinter event loop
root.mainloop()