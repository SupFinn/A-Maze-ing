from typing import Any, Dict, Tuple
from collections import deque
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

    def solve_bfs(self, entry: Tuple[int, int], exit: Tuple[int, int]) -> str:
        queue = deque()
        queue.append(entry)

        visited = set()
        visited.add(entry)
        parent = {}

        while queue:
            x, y = queue.popleft()
            cell = self.grid[y][x]
            if (x, y) == exit:
                break
            
            if not cell.north and (x, y-1) not in visited:
                queue.append((x, y-1))
                visited.add((x, y-1))
                parent[(x, y-1)] = ((x, y), "N")

            if not cell.east and (x+1, y) not in visited:
                queue.append((x+1, y))
                visited.add((x+1, y))
                parent[(x+1, y)] = ((x, y), "E")

            if not cell.south and (x, y+1) not in visited:
                queue.append((x, y+1))
                visited.add((x, y+1))
                parent[(x, y+1)] = ((x, y), "S")

            if not cell.west and (x-1, y) not in visited:
                queue.append((x-1, y))
                visited.add((x-1, y))
                parent[(x-1, y)] = ((x, y), "W")
        
        path = []
        current = exit
        while current != entry:
            current, direction = parent[current]
            path.append(direction)
        path.reverse()
        return "".join(path)


    def write_maze_hex(self,
                       filename: str,
                       entry: Tuple[int,int],
                       exit: Tuple[int,int],
                       path: str) -> None:

        with open(filename, "w") as f:
            for y in range(self.height):
                row = []
                for x in range(self.width):
                    cell = self.grid[y][x]
                    value = 0
                    if cell.north:
                        value += 1
                    if cell.east:
                        value += 2
                    if cell.south:
                        value += 4
                    if cell.west:
                        value += 8
                    row.append(format(value, "X"))
                f.write(" ".join(row) + "\n")
            f.write(f"{entry[0]}, {entry[1]}\n")
            f.write(f"{exit[0]}, {exit[1]}\n")
            f.write(f"{path}\n")
                
#    N
#  W   E
#    S
