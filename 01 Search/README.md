# 2023_02 CSE4185 Assignment01: Maze Game

## Implement:
BFS,IDS와 A * Algorithm을 활용한 최단 경로 찾기 

## Requirements:
```
pip install pygame
```
## How to run the code:

```
usage: main.py [-h] [--method {bfs,ids,astar,astar_four_circles,astar_many_circles}] [--scale SCALE]
              [--speed speed] [--keyboard] [--save SAVE]
              filename
```

Examples of how to run main.py:
```
python main.py category/stage1/small.txt --method bfs
```
```
python main.py category/stage1/small.txt --scale 30 --speed 10 --keyboard
```

For help run:
```
python main.py -h
```
Help Output:
```
CSE4185 Assignment01: Maze Game

positional arguments:
  filename              path to maze file [REQUIRED]

optional arguments:
  -h, --help            show this help message and exit
  --method {bfs,dfs,astar,astar_four_circles,astar_many_circles}
                        search method - default bfs
  --scale SCALE         scale - default: 20
  --speed SPEED         speed for the display - default 15
  --keyboard            you can play the game - default False
  --save SAVE           save output to image file - default not saved
```
