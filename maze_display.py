"""
Maze display module for ASCII visualization with ANSI colors.
"""
from typing import Tuple, Optional, Set
import sys
import os


class MazeDisplay:
    """
    Handles visualization of mazes in ASCII format with ANSI colors.
    
    Attributes:
        width: Maze width in cells
        height: Maze height in cells
        colors: Dictionary of color configurations
    """
    
    # ANSI color codes
    RESET = "\033[0m"
    
    # Foreground colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Background colors (normal)
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_GRAY = "\033[100m"
    
    # Background colors (bright)
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"
    
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize maze display.
        
        Args:
            width: Maze width in cells
            height: Maze height in cells
        """
        self.width: int = width
        self.height: int = height
        
        # Default color configuration
        self.colors = {
            'entry': self.GREEN,                    # Bright green for start (S)
            'exit': self.RED,                       # Bright red for exit (E)
            'highlight': self.BG_BRIGHT_MAGENTA,    # Magenta block for generation animation
            'pattern': self.BG_BRIGHT_YELLOW,       # Yellow background for '42' pattern
            'path': self.YELLOW,                    # Yellow # for solution path
            'wall': self.CYAN,                      # Cyan walls (great contrast)
            'unvisited': self.BG_GRAY,              # Gray blocks for unvisited cells
            'search': self.CYAN                     # Cyan # for BFS search animation
        }
        
    def set_color(self, element: str, color: str) -> None:
        """
        Set color for a specific maze element.
        
        Args:
            element: Element name ('entry', 'exit', 'highlight', 'pattern', 'path', 'wall')
            color: ANSI color code
        """
        if element in self.colors:
            self.colors[element] = color
    
    def set_pattern_color(self, color_name: str) -> None:
        """
        Set the color for the '42' pattern using predefined colors.
        
        Args:
            color_name: Color name ('cyan', 'yellow', 'magenta', 'blue', 'red', 'green')
        """
        color_map = {
            'cyan': self.BG_BRIGHT_CYAN,
            'yellow': self.BG_BRIGHT_YELLOW,
            'magenta': self.BG_BRIGHT_MAGENTA,
            'blue': self.BG_BRIGHT_BLUE,
            'red': self.BG_BRIGHT_RED,
            'green': self.BG_BRIGHT_GREEN,
            'white': self.BG_BRIGHT_WHITE,
            'black': self.BG_BRIGHT_BLACK,
            'gray': self.BG_GRAY
        }
        
        if color_name.lower() in color_map:
            self.colors['pattern'] = color_map[color_name.lower()]
        else:
            print(f"Warning: Unknown color '{color_name}'. Using default.")

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        import os
        os.system('clear')

    def path_to_cells(self, 
                     entry: Tuple[int, int], 
                     path: str) -> Set[Tuple[int, int]]:
        """
        Convert path string to set of cell coordinates.
        
        Args:
            entry: Starting position (x, y)
            path: Path string (N, E, S, W directions)
            
        Returns:
            Set of (x, y) coordinates along the path
        """
        x, y = entry
        cells: Set[Tuple[int, int]] = {(x, y)}

        for move in path:
            if move == "N":
                y -= 1
            elif move == "S":
                y += 1
            elif move == "E":
                x += 1
            elif move == "W":
                x -= 1
            cells.add((x, y))

        return cells
        
    def display_ascii(self,
                    grid: list,
                    entry: Tuple[int, int],
                    exit: Tuple[int, int],
                    pattern_cells: Set[Tuple[int, int]],
                    path: Optional[str] = None,
                    highlight: Optional[Tuple[int, int]] = None,
                    show_generation: bool = False,
                    visited_cells: Optional[Set[Tuple[int, int]]] = None) -> None:
        """
        Display maze in ASCII format with ANSI colors.
        
        Args:
            grid: 2D list of Cell objects
            entry: Entry position (x, y)
            exit: Exit position (x, y)
            pattern_cells: Set of cells that form the '42' pattern
            path: Optional solution path to display
            highlight: Optional cell to highlight (used during generation)
            show_generation: Whether to show unvisited cells as blocks during generation
            visited_cells: Optional set of visited cells during BFS (for animation)
        """
        path_cells: Set[Tuple[int, int]] = set()
        if path:
            path_cells = self.path_to_cells(entry, path)

        # Top border with wall color
        for x in range(self.width):
            print(f"{self.colors['wall']}+---{self.RESET}", end="")
        print(f"{self.colors['wall']}+{self.RESET}")

        # Maze body
        for y in range(self.height):
            # West walls and cell content
            for x in range(self.width):
                cell = grid[y][x]
                
                # West wall with color
                if cell.west:
                    print(f"{self.colors['wall']}|{self.RESET}", end="")
                else:
                    print(" ", end="")

                # Cell content priority order
                if (x, y) == entry:
                    print(f"{self.colors['entry']} S {self.RESET}", end="")
                elif (x, y) == exit:
                    print(f"{self.colors['exit']} E {self.RESET}", end="")
                elif highlight and (x, y) == highlight:
                    print(f"{self.colors['highlight']}   {self.RESET}", end="")  # Block during animation
                elif (x, y) in pattern_cells:
                    # Display '42' pattern as solid colored block
                    print(f"{self.colors['pattern']}   {self.RESET}", end="")
                elif show_generation and not cell.visited:
                    # During generation: show unvisited cells as gray blocks
                    print(f"{self.colors['unvisited']}   {self.RESET}", end="")
                elif visited_cells and (x, y) in visited_cells:
                    # During solving: show visited cells as #
                    print(f"{self.colors['search']} # {self.RESET}", end="")  # Cyan # for search
                elif path and (x, y) in path_cells:
                    # Final solution path as #
                    print(f"{self.colors['path']} # {self.RESET}", end="")  # Magenta # for solution
                else:
                    print("   ", end="")

            # East border with color
            print(f"{self.colors['wall']}|{self.RESET}")

            # South walls with color
            for x in range(self.width):
                cell = grid[y][x]
                if cell.south:
                    print(f"{self.colors['wall']}+---{self.RESET}", end="")
                else:
                    print(f"{self.colors['wall']}+{self.RESET}   ", end="")
            print(f"{self.colors['wall']}+{self.RESET}")