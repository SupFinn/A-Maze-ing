#!/usr/bin/python3

from maze_generator import read_config

def main():
    try:
        config = read_config("config.txt")
        print("Config loaded successfully!")
        print(config)
    except Exception as e:
        print(f"Error reading config: {e}")


if __name__ == "__main__":
    main()