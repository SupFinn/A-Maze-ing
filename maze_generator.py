from typing import Tuple, Optional, Set, Dict
from collections import deque
import random
import time
from maze_display import MazeDisplay


class Cell:
    def __init__(self) -> None:
        """Initialize a cell with all walls closed."""
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False

class MazeGenerator:
    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        self.width: int = width
        self.height: int = height
        self.pattern_cells: Set[Tuple[int, int]] = set()
        
        if seed is not None:
            random.seed(seed)
            
        self.grid: list = []
        for y in range(self.height):
            row: list = []
            for x in range(self.width):
                row.append(Cell())
            self.grid.append(row)

    def add_42_pattern(self) -> bool:
        pattern = [
            "# # ###",
            "# #   #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Warning: Maze too small to add '42' pattern.")
            return False

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        self.pattern_cells = set()

        for row_num, row in enumerate(pattern):
            for col_num, char in enumerate(row):
                if char == '#':
                    maze_x = start_x + col_num
                    maze_y = start_y + row_num
                    
                    cell = self.grid[maze_y][maze_x]
                    cell.north = True
                    cell.east = True
                    cell.south = True
                    cell.west = True
                    cell.visited = True
                    
                    self.pattern_cells.add((maze_x, maze_y))
        
        return True

    def generate_backtracking(self, 
                            entry: Tuple[int, int],
                            display: Optional[MazeDisplay] = None,
                            delay: float = 0.05) -> None:
        entry_x, entry_y = entry
        start_cell = self.grid[entry_y][entry_x]
        start_cell.visited = True

        stack: list = [(entry_x, entry_y)]
        
        while stack:
            x, y = stack[-1]
            neighbors: list = []
            
            if y > 0 and not self.grid[y-1][x].visited:
                if (x, y-1) not in self.pattern_cells:
                    neighbors.append((x, y-1))
                    
            if x < self.width - 1 and not self.grid[y][x+1].visited:
                if (x+1, y) not in self.pattern_cells:
                    neighbors.append((x+1, y))
                    
            if y < self.height - 1 and not self.grid[y+1][x].visited:
                if (x, y+1) not in self.pattern_cells:
                    neighbors.append((x, y+1))
                    
            if x > 0 and not self.grid[y][x-1].visited:
                if (x-1, y) not in self.pattern_cells:
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
                
                if display is not None:
                    display.clear_screen()
                    display.display_ascii(self.grid, entry, entry, 
                                        self.pattern_cells, 
                                        highlight=(next_x, next_y),
                                        show_generation=True)
                    time.sleep(delay)
            else:
                stack.pop()


    def reset_visited(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].visited = False


    def solve_bfs(self, entry: Tuple[int, int], exit: Tuple[int, int],
                display: Optional[MazeDisplay] = None,
                delay: float = 0.05) -> str:
            queue: deque = deque()
            queue.append(entry)

            visited: Set[Tuple[int, int]] = set()
            visited.add(entry)
            parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

            while queue:
                x, y = queue.popleft()
                cell = self.grid[y][x]

                if display is not None:
                    display.clear_screen()
                    display.display_ascii(self.grid, entry, exit, 
                                        self.pattern_cells,
                                        highlight=(x, y),
                                        show_generation=False,
                                        visited_cells=visited)
                    time.sleep(delay)
                
                if (x, y) == exit:
                    break
                if y > 0 and not cell.north and (x, y-1) not in visited:
                    queue.append((x, y-1))
                    visited.add((x, y-1))
                    parent[(x, y-1)] = ((x, y), "N")
                if x < self.width - 1 and not cell.east and (x+1, y) not in visited:
                    queue.append((x+1, y))
                    visited.add((x+1, y))
                    parent[(x+1, y)] = ((x, y), "E")
                if y < self.height - 1 and not cell.south and (x, y+1) not in visited:
                    queue.append((x, y+1))
                    visited.add((x, y+1))
                    parent[(x, y+1)] = ((x, y), "S")
                if x > 0 and not cell.west and (x-1, y) not in visited:
                    queue.append((x-1, y))
                    visited.add((x-1, y))
                    parent[(x-1, y)] = ((x, y), "W")

            path: list = []
            current = exit
            while current != entry:
                if current not in parent:
                    return ""
                current, direction = parent[current]
                path.append(direction)
            path.reverse()
            return "".join(path)

    def write_maze_hex(self,
                       filename: str,
                       entry: Tuple[int, int],
                       exit: Tuple[int, int],
                       path: str) -> None:
        with open(filename, "w") as f:
            for y in range(self.height):
                row: list = []
                for x in range(self.width):
                    cell = self.grid[y][x]
                    value: int = 0
                    if cell.north:
                        value += 1
                    if cell.east:
                        value += 2
                    if cell.south:
                        value += 4
                    if cell.west:
                        value += 8
                    row.append(format(value, "X"))
                f.write("".join(row) + "\n")
            f.write(f"\n{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{path}\n")

    def break_walls(self, chance: float = 0.1) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue
                    
                if random.random() < chance:
                    cell = self.grid[y][x]
                    direction = random.choice(["N", "E", "S", "W"])

                    if direction == "N" and y > 0:
                        if (x, y-1) not in self.pattern_cells:
                            cell.north = False
                            self.grid[y-1][x].south = False
                    elif direction == "S" and y < self.height - 1:
                        if (x, y+1) not in self.pattern_cells:
                            cell.south = False
                            self.grid[y+1][x].north = False
                    elif direction == "E" and x < self.width - 1:
                        if (x+1, y) not in self.pattern_cells:
                            cell.east = False
                            self.grid[y][x+1].west = False
                    elif direction == "W" and x > 0:
                        if (x-1, y) not in self.pattern_cells:
                            cell.west = False
                            self.grid[y][x-1].east = False