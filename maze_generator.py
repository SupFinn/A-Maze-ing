from typing import Any, Dict, Tuple
import random

def read_config(filename: str) -> Dict[str, Any]:
    config: Dict = {}
    with open(filename) as config_file:
        for line in config_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split('=', 1)
            if key == "WIDTH" or key == "HEIGHT":
                value = int(value)
            elif key == "ENTRY" or key == "EXIT":
                parts = value.split(",")
                value = tuple(int(p) for p in parts)
            elif key == "PERFECT":
                value = value.strip().lower() == "true"
            config[key] = value
    return config


class Cell:
    def __init__(self):
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = []
        for y in range (self.height):
            row = []
            for x in range(self.width):
                row.append(Cell())
            self.grid.append(row)


    def generate_backtracking(self,  entry: Tuple[int,int]):
        entry_x, entry_y = entry
        start_cell = self.grid[entry_y][entry_x]
        start_cell.visited = True

        stack = [(entry_x, entry_y)]
        while stack:
            x, y = stack[-1]
            neighbors = []
            if y > 0 and not self.grid[y-1][x].visited:
                neighbors.append((x, y-1))
            if x < self.width - 1 and not self.grid[y][x+1].visited:
                neighbors.append((x+1, y))
            if y < self.height - 1 and not self.grid[y+1][x].visited:
                neighbors.append((x, y+1))
            if x > 0 and not self.grid[y][x-1].visited:
                neighbors.append((x-1, y))
            
            if neighbors:
                next_x, next_y = random.choice(neighbors)
                current = self.grid[y][x]
                neighbor = self.grid[next_y][next_x]
                if next_y < y:
                    current.north = False
                    neighbor.south = False
                elif next_y > y:
                    current.south = False
                    neighbor.north = False
                elif next_x > x:
                    current.east = False
                    neighbor.west = False
                elif next_x < x:
                    current.west = False
                    neighbor.east = False
                neighbor.visited = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
                
                
                
#    N
#  W   E
#    S