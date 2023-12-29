from maze import Maze

############# Write Your Library Here ##########
import heapq
from collections import deque
import math

################################################


def search(maze, func):
    return {
        "bfs": bfs,
        "ids":ids,
        "astar": astar,
        "astar_four_circles": astar_four_circles,
        "astar_many_circles": astar_many_circles
    }.get(func)(maze)

def bfs(maze:Maze):
    """
    [Problem 01] 제시된 stage1 맵 세 가지를 BFS를 구현하여 목표지점을 찾는 경로를 return하시오.
    """
    start_point=maze.startPoint()
    path=[]
    ####################### Write Your Code Here ################################
    goal_points=maze.circlePoints()
    if len(goal_points) == 0:
        return []
    goal_point = goal_points[0]
    

    #make queue , add to start point
    queue = [start_point]
    #visited set
    visited = set([start_point])
    parents = {}
    
    idx=0
    while idx< len(queue):
        current = queue[idx]  #queue output -> current point
        idx += 1 
        
        #if current point is goal point, construct path
        if current == goal_point:
            path = [current]
            while current in parents:
                current = parents[current]
                path.append(current)
            path.reverse()
            return path
        
        #get the neighbor point and add non visited point to queue
        for neighbor in maze.neighborPoints(current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parents[neighbor] = current
    return []
 # def get_neighbors(pos):
    #     r,c =pos
    #     direction =[(0,1),(1,0),(0,-1),(-1,0)]
    #     neighbors=[]
    #     for dr, dc in direction: 
    #         next_r, next_c =r+ dr, c + dc  
    #         if not maze.isWall(next_r, next_c):
    #             neighbors.append((next_r, next_c))
    #     return neighbors
    ############################################################################

def ids(maze:Maze):
    """
    [Problem 02] 제시된 stage1 맵 세 가지를 IDS를 구현하여 목표지점을 찾는 경로를 return하시오.
    """
    start_point=maze.startPoint()
    path=[]
    ####################### Write Your Code Here ################################
    goal_points=maze.circlePoints()
    if len(goal_points) ==0: 
        return []
    goal_point=goal_points[0]
    
    depth = 0
    while True:  #while search goal
        stack = [(start_point, [start_point])]
        VisitedDepth = set()

        while stack:  #while stack is empty
            node, current_path = stack.pop()
            #if current point is goal , reutrn current_path
            if node == goal_point:
                return current_path
            if len(current_path) > depth:  
                continue
            #if the point does not visited, add visited point
            for neighbor in maze.neighborPoints(node[0], node[1]):
                if neighbor not in VisitedDepth:
                    VisitedDepth.add(neighbor)
                    stack.append((neighbor, current_path + [neighbor]))
        

        depth += 1
    #############################################################################

# Manhattan distance
def stage1_heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def astar(maze:Maze):
    """
    [Problem 03] 제시된 stage1 맵 세가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 위에서 정의한 stage1_heuristic function(manhattan_dist)을 사용할 것.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    goal_points=maze.circlePoints()
    if len(goal_points) ==0: 
        return []
    goal_point=goal_points[0]

    # f,g,point
    List=[(stage1_heuristic(start_point,goal_point),0,start_point)]
    
    g_values={start_point: 0} #initalize
    parents={}

    while List:  #do while open list is empty
        _, current_g, current = heapq.heappop(List)
        
        #if current node id goal , construct path and return path
        if current==goal_point:
            path=[current]
            while current in parents:
                current =parents[current]
                path.append(current)
            path.reverse()
            return path
        
        #check the neighbor point 
        for neighbor in maze.neighborPoints(current[0], current[1]):
            new_g=current_g+1 #update new g
            if neighbor not in g_values or new_g < g_values[neighbor]:
                g_values[neighbor]=new_g
                h=stage1_heuristic(neighbor, goal_point)
                f=new_g+ h
                heapq.heappush(List, (f, new_g, neighbor))
                parents[neighbor] = current  #the current node -> parent of meighbor node
    return []



    


    ############################################################################


####################### Write Your Code Here ################################
def stage2_heuristic_2(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def stage2_heuristic(p1,goals):
    return min([stage2_heuristic_2(p1,goal) for goal in goals])   
############################################################################

#어떤 circlepoint에서 goal에 도달하는 길을 찾는 함수
def astar_search(maze, start_point, end_points):
    start_cost = stage2_heuristic(start_point, end_points)
    List = [(start_cost, start_point, [])]
    visited = set()

    while List:
        _, current, current_path = heapq.heappop(List)

        if current in visited:
            continue

        if current in end_points:
            return current_path + [current]
        visited.add(current)

        for neighbor in maze.neighborPoints(current[0], current[1]):
            if neighbor in current_path:
                continue
            new_path = current_path + [current]
            g_cost = len(new_path)
            h_cost = stage2_heuristic(neighbor, end_points)
            f = g_cost + h_cost
            heapq.heappush(List, (f, neighbor, new_path))

    return []

def astar_four_circles(maze:Maze):
    """
    [Problem 04] 제시된 stage2 맵 세 가지를 A* Algorithm을 통해 최단경로를 return하시오.
    (Heuristic Function은 직접 정의할것 )
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ###############################
    all_goal_points = maze.circlePoints()

    if len(all_goal_points) != 4:
        return []

    path = astar_search(maze, maze.startPoint(), all_goal_points)

    if not path:
        return []

    last_visited = path[-1]
    all_goal_points.remove(last_visited)

    for goal in all_goal_points:
        segment = astar_search(maze, last_visited, [goal]) #모든 circle에 대해 goal까지의 길이를 찾는다
        if not segment:
            return []
        
        for i in range(1, len(segment)):
            path.append(segment[i])
        
        last_visited = segment[-1]
    objective_points = []
    
    for point in maze.circlePoints():
        if maze.isObjective(point[0], point[1]):
            objective_points.append(point)

    final_path = astar_search(maze, last_visited, objective_points)

    if not final_path:
        return []
    
    for i in range(1, len(final_path)):
        path.append(final_path[i])

    return path


            


    ############################################################################


####################### Write Your Code Here ###############################
def stage3_heuristic():
    pass
############################################################################

def astar_many_circles(maze: Maze):
    """
    [Problem 05] 제시된 stage3 맵 다섯 가지를 A* Algorithm을 통해 최단 경로를 return하시오.
    (Heuristic Function은 직접 정의 하고, minimum spanning tree를 활용하도록 한다.)
    """
    start_point = maze.startPoint()
    path = []
    ####################### Write Your Code Here ################################
    
    ############################################################################
    