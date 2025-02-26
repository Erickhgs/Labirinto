# -*- coding: utf-8 -*-
import time
from maze import Maze
from collections import deque

s = deque()


maze_csv_path = "labirinto1.txt"  # Substitua pelo caminho correto
maze = Maze() 

maze.load_from_csv(maze_csv_path)

# Exibir o lab
maze.run()
maze.init_player()




