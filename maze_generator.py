"""
Maze generator using recursive backtracking algorithm.
"""
from typing import Tuple, Optional, Set, Dict
from collections import deque
import random
import time
from maze_display import MazeDisplay

class Cell:
    """
    Represents a single cell in the maze with four walls.
    
    Attributes:
        north: Whether the north wall exists
        east: Whether the east wall exists
        south: Whether the south wall exists
        west: Whether the west wall exists
        visited: Whether the cell has been visited during generation
    """
    
    def __init__(self) -> None:
        """Initialize a cell with all walls closed."""
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False

class MazeGenerator:
    """
    Maze generator using recursive backtracking algorithm.
    
    Attributes:
        width: Number of cells horizontally
        height: Number of cells vertically
        grid: 2D list of Cell objects
        pattern_cells: Set of cells that form the '42' pattern
    """
    
    def __init__(self, width: int, height: int, seed: Optional[int] = None) -> None:
        """
        Initialize maze generator.
        
        Args:
            width: Maze width in cells
            height: Maze height in cells
            seed: Optional random seed for reproducibility
        """
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
        """
        Add a '42' pattern in the center of the maze.
        
        The pattern consists of fully closed cells forming the digits '4' and '2'
        with proper spacing between them.
        
        Returns:
            True if successful, False if the maze is too small
        """
        NUMBER_42_PATTERN = [
            # Digit '4' - 3 blocks wide
            [
                [1, 0, 1],  # # #
                [1, 0, 1],  # # #
                [1, 1, 1],  # ###
                [0, 0, 1],  #   #
                [0, 0, 1],  #   #
            ],
            # Digit '2' - 3 blocks wide
            [
                [1, 1, 1],  # ###
                [0, 0, 1],  #   #
                [1, 1, 1],  # ###
                [1, 0, 0],  # #
                [1, 1, 1],  # ###
            ]
        ]

        pattern_height: int = 5
        pattern_width: int = 7  # 3 (for '4') + 1 (space) + 3 (for '2')

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Warning: Maze too small to add '42' pattern.")
            return False

        # Compute top-left coordinates for centering
        top_left_x: int = (self.width - pattern_width) // 2
        top_left_y: int = (self.height - pattern_height) // 2

        self.pattern_cells = set()
        digit_offsets = [0, 4]  # '4' starts at 0, '2' starts at 4 (3 + 1 space)

        for d_index, digit in enumerate(NUMBER_42_PATTERN):
            for y, row in enumerate(digit):
                for x, cell_value in enumerate(row):
                    maze_x: int = top_left_x + x + digit_offsets[d_index]
                    maze_y: int = top_left_y + y
                    if cell_value == 1:
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
                            animate: bool = False,
                            delay: float = 0.05) -> None:
        """
        Generate maze using recursive backtracking algorithm.
        
        Args:
            entry: Starting position (x, y)
            display: Optional MazeDisplay instance for visualization
            animate: Whether to show animation during generation
            delay: Delay between animation frames in seconds
        """
        entry_x, entry_y = entry
        start_cell = self.grid[entry_y][entry_x]
        start_cell.visited = True

        stack: list = [(entry_x, entry_y)]
        
        while stack:
            x, y = stack[-1]
            neighbors: list = []
            
            # Check all four directions for unvisited neighbors
            # Skip cells that are part of the '42' pattern
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
                
                # Remove walls between current and chosen neighbor
                if next_y < y:  # Moving North
                    current.north = False
                    neighbor.south = False
                elif next_y > y:  # Moving South
                    current.south = False
                    neighbor.north = False
                elif next_x > x:  # Moving East
                    current.east = False
                    neighbor.west = False
                elif next_x < x:  # Moving West
                    current.west = False
                    neighbor.east = False
                    
                neighbor.visited = True
                stack.append((next_x, next_y))
                
                # Animation - show unvisited cells as blocks
                if animate and display is not None:
                    display.clear_screen()
                    display.display_ascii(self.grid, entry, entry, 
                                        self.pattern_cells, 
                                        highlight=(next_x, next_y),
                                        show_generation=True)  # ← This shows blocks!
                    time.sleep(delay)
            else:
                stack.pop()

    def reset_visited(self) -> None:
        """Reset the visited flag for all cells."""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].visited = False


    def solve_bfs(self, entry: Tuple[int, int], exit: Tuple[int, int],
                display: Optional[MazeDisplay] = None,
                animate: bool = False,
                delay: float = 0.05) -> str:
            queue: deque = deque()
            queue.append(entry)

            visited: Set[Tuple[int, int]] = set()
            visited.add(entry)
            parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

            while queue:
                x, y = queue.popleft()
                cell = self.grid[y][x]
                if animate and display is not None:
                    display.clear_screen()
                    # Convert visited set to path string for display
                    display.display_ascii(self.grid, entry, exit, 
                                        self.pattern_cells,
                                        highlight=(x, y),
                                        show_generation=False,
                                        visited_cells=visited)
                    time.sleep(delay)
                
                if (x, y) == exit:
                    break
                
                # Check North
                if y > 0 and not cell.north and (x, y-1) not in visited:
                    queue.append((x, y-1))
                    visited.add((x, y-1))
                    parent[(x, y-1)] = ((x, y), "N")

                # Check East
                if x < self.width - 1 and not cell.east and (x+1, y) not in visited:
                    queue.append((x+1, y))
                    visited.add((x+1, y))
                    parent[(x+1, y)] = ((x, y), "E")

                # Check South
                if y < self.height - 1 and not cell.south and (x, y+1) not in visited:
                    queue.append((x, y+1))
                    visited.add((x, y+1))
                    parent[(x, y+1)] = ((x, y), "S")

                # Check West
                if x > 0 and not cell.west and (x-1, y) not in visited:
                    queue.append((x-1, y))
                    visited.add((x-1, y))
                    parent[(x-1, y)] = ((x, y), "W")

            # Reconstruct path
            path: list = []
            current = exit
            while current != entry:
                if current not in parent:
                    # No path found
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
        """
        Write maze to file in hexadecimal format.
        
        Format:
        - Each cell encoded as single hex digit (0-F)
        - Bit 0: North wall, Bit 1: East wall
        - Bit 2: South wall, Bit 3: West wall
        
        Args:
            filename: Output file path
            entry: Entry position (x, y)
            exit: Exit position (x, y)
            path: Solution path as direction string
        """
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
        """
        Break random walls to create an imperfect maze.
        
        Args:
            chance: Probability (0-1) of breaking a wall for each cell
        """
        for y in range(self.height):
            for x in range(self.width):
                # Don't break walls in the '42' pattern
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