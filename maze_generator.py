from typing import Any, Dict, Tuple
import random

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


    def write_maze_hex(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                

                
#    N
#  W   E
#    S