#!/usr/bin/python3

import sys
from config_validation import read_config, validation

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        return
    config_file = sys.argv[1]
    try:
        config = read_config(config_file)
        validation(config)
    except Exception as e:
        print(e)
        return

    print(config)

if __name__ == "__main__":
    main()