#!/usr/bin/env python3
"""
A-Maze-ing: Maze generator with animated visualization.

This project has been created as part of the 42 curriculum by SupFinnthis.
"""
import sys
from config_validation import read_config, validation
from maze_generator import MazeGenerator
from maze_display import MazeDisplay

def clear_screen() -> None:
    """Clear the screen."""
    print("\033[2J\033[H", end="")
    sys.stdout.flush()

def display_menu() -> None:
    """Display the interactive menu."""
    print("\n" + "="*50)
    print("         MAZE CONTROL MENU")
    print("="*50)
    print("  1. Re-generate maze")
    print("  2. Show/Hide solution path")
    print("  3. Change wall colors")
    print("  4. Change '42' pattern color")
    print("  q. Quit")
    print("="*50)


def get_user_choice() -> str:
    """Get user menu choice."""
    choice = input("\nEnter your choice: ").strip().lower()
    return choice


def choose_color(current: str) -> str:
    """Let user choose a color."""
    print(f"\nCurrent color: {current.upper()}")
    print("Available colors:")
    print("  1. Red")
    print("  2. Green")
    print("  3. Yellow")
    print("  4. Blue")
    print("  5. Magenta")
    print("  6. Cyan")
    print("  7. White")
    
    color_map = {
        '1': 'red',
        '2': 'green',
        '3': 'yellow',
        '4': 'blue',
        '5': 'magenta',
        '6': 'cyan',
        '7': 'white'
    }
    
    choice = input("Choose color (1-7): ").strip()
    return color_map.get(choice, current)


def main() -> None:
    """Main entry point for maze generator."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
        
    config_file: str = sys.argv[1]
    
    try:
        config = read_config(config_file)
        validation(config)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    # Extract required configuration from file
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    entry: tuple = config["ENTRY"]
    exit_: tuple = config["EXIT"]
    output: str = config["OUTPUT_FILE"]
    perfect: bool = config["PERFECT"]
    
    # Settings
    show_path: bool = False
    animation_speed: float = 0.02
    pattern_color: str = "yellow"
    wall_color: str = "white"
    
    # Create display
    display = MazeDisplay(width, height)
    display.set_pattern_color(pattern_color)
    
    # Generate initial maze with animation
    clear_screen()
    print("Generating maze...\n")
    print("Watch as the maze carves through the solid blocks!\n")
    
    maze = MazeGenerator(width, height)
    maze.add_42_pattern()
    maze.generate_backtracking(entry, display=display, 
                              animate=True, delay=animation_speed)
    maze.reset_visited()
    
    if not perfect:
        maze.break_walls(chance=0.1)
    
    # Solve maze WITH ANIMATION
    print("\nSolving maze...\n")
    path: str = maze.solve_bfs(entry, exit_, display=display,
                               animate=True, delay=animation_speed)
    
    # Save to file
    maze.write_maze_hex(output, entry, exit_, path)
    
    # Display final result
    clear_screen()
    print("Maze generation and solving complete!\n")
    display.display_ascii(maze.grid, entry, exit_, maze.pattern_cells,
                         path=path, show_generation=False)
    
    # Interactive loop
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == '1':
            # Re-generate maze
            clear_screen()
            print("Regenerating maze...\n")
            print("Watch as the maze carves through the solid blocks!\n")
            
            maze = MazeGenerator(width, height)
            maze.add_42_pattern()
            maze.generate_backtracking(entry, display=display, 
                                      animate=True, delay=animation_speed)
            maze.reset_visited()
            
            if not perfect:
                maze.break_walls(chance=0.1)
            
            # Solve with animation
            print("\nSolving maze...\n")
            path = maze.solve_bfs(entry, exit_, display=display,
                                 animate=True, delay=animation_speed)
            maze.write_maze_hex(output, entry, exit_, path)
            
            clear_screen()
            print("Maze regenerated and solved!\n")
            display.display_ascii(maze.grid, entry, exit_, maze.pattern_cells,
                                path if show_path else None,
                                show_generation=False)
        
        elif choice == '2':
            # Toggle path display
            show_path = not show_path
            clear_screen()
            if show_path:
                print("Solution path: SHOWN\n")
            else:
                print("Solution path: HIDDEN\n")
            display.display_ascii(maze.grid, entry, exit_, maze.pattern_cells,
                                path if show_path else None,
                                show_generation=False)
        
        elif choice == '3':
            # Change wall colors
            print("\nChange wall color (affects all walls)")
            new_color = choose_color(wall_color)
            wall_color = new_color
            
            # Map to ANSI color codes
            ansi_map = {
                'red': display.RED,
                'green': display.GREEN,
                'yellow': display.YELLOW,
                'blue': display.BLUE,
                'magenta': display.MAGENTA,
                'cyan': display.CYAN,
                'white': display.WHITE
            }
            
            display.set_color('wall', ansi_map.get(wall_color, display.WHITE))
            
            clear_screen()
            print(f"Wall color changed to: {wall_color.upper()}\n")
            display.display_ascii(maze.grid, entry, exit_, maze.pattern_cells,
                                path if show_path else None,
                                show_generation=False)
        
        elif choice == '4':
            # Change pattern color
            print("\nChange '42' pattern color")
            new_color = choose_color(pattern_color)
            pattern_color = new_color
            display.set_pattern_color(pattern_color)
            
            clear_screen()
            print(f"Pattern color changed to: {pattern_color.upper()}\n")
            display.display_ascii(maze.grid, entry, exit_, maze.pattern_cells,
                                path if show_path else None,
                                show_generation=False)
        
        elif choice == 'q':
            # Quit
            clear_screen()
            print("Saving final maze to file...")
            maze.write_maze_hex(output, entry, exit_, path)
            print(f"Maze saved to: {output}")
            print("\nGoodbye!")
            sys.exit(0)
        
        else:
            print("\nInvalid choice! Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()