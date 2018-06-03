#!/usr/bin/python3.5

# ^^ note the python directive on the first line
# COMP 9414 agent initiation file 
# requires the host is running before the agent
# designed for python 3.6
# typical initiation would be (file in working directory, port = 31415)
#        python3 agent.py -p 31415
# created by Leo Hoare
# with slight modifications by Alan Blair

# Modified by Oscar Downing (z5114817) and Tim Thacker (z5115699)

# === DESIGN ===

# The data structure used to keep track of all the known parts of the map is a 160 x 160 2D array. 
# This size is to accommodate an 80 x 80 map which starts the agent in the corner.
# In our data structure the agent starts in the middle so whichever way the map grows it will 
# never go past the edge of the array.


# Each time a new map segment is received, the map data structure is updated with the new information.
# A Breadth first search is then performed on all of the objects

# we have different versions of the bfs avoiding certain objects and allowing some to be connections
# please see the functions for further detail

# We chose breadth first search because it always produces an optimal solution.
# Within the BFS we used a dictionary / hash table for the graph (list of connections)

# If a path to the treasure/key/axe/stone/tree/door cannot be found, the agent is 
# instructed to move around and discover more of the map.

# This is repeated until a path can be found to the treasure and paths can be found to all the tools required to get to the treasure.
# The path to the treasure is analysed to determine which tools are required.

# This algorithm was chosen because a solution can be generated if a possible path to the treasure is found
# and and to all the required tools

import sys
import socket
import collections
import random
import time
import copy
from collections import deque

# keep track of tools
tools = []

# Obstacles  Tools
# T   tree    a   axe
# -   door    k   key
# ~   water   o   stepping stone
# *   wall    $   treasure    

# obstacles
wall, clear, covered, edge = "*", " ", "O", "."
tree, door, water = "T", "-", "~"

# tools
key, axe, stone, treasure = "k", "a", "o", "$"

# the x, y position change of the player
shift_x = 0
shift_y = 0

# position of the player
sx = 79
sy = 79

# current position
pos = "^"

# declaring visible grid to agent
view   = [[''  for _ in range(5)]   for _ in range(5)]

# the map of we build from 5x5 grids
my_map = [['?' for _ in range(160)] for _ in range(160)]


# convert a 2d maze into a graph rep with exploring allowed
def special_maze2graph(maze, goal):
    global tools
    height = 160
    width = 160
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == wall}

    if key in tools and goal == door:
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == tree:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == tree:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    elif axe in tools and goal == tree:
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    else :
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == tree and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == tree and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))

    return graph

# convert a 2d maze into a graph rep with exploring not allowed (don't search unknown areas)
def maze2graph(maze, goal):
    global tools
    height = 160
    width = 160
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == wall}

    if key in tools and goal == door:
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == "?" and not maze[row + 1][col] == tree:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == "?" and not maze[row][col + 1] == tree:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    elif axe in tools and goal == tree:
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == "?" and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == "?" and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    else :  
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == "?" and not maze[row + 1][col] == tree and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == "?" and not maze[row][col + 1] == tree and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
        
    return graph

# standard bfs - avoids water unless we have a boat
def bfs(maze, goal, x, y):
    global tools
    queue = deque([("",(x,y))])
    visited = set()
    graph = maze2graph(maze,goal)
    i = 0

    while queue:
        path, current = queue.popleft()
        if maze[current[0]][current[1]] == goal and i > 0:# and current[0] != x and current[1] != y:
            path += "g"
            return path
        if current in visited or (maze[current[0]][current[1]] == water and tree not in tools) :
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
        i+=1
    return None

#exploring bfs - goes to unknown areas including crossing water
def exploring_bfs(maze, goal, x, y):
    global tools
    queue = deque([("",(x,y))])
    visited = set()
    graph = special_maze2graph(maze,goal)
    i = 0

    while queue:
        path, current = queue.popleft()
        if maze[current[0]][current[1]] == goal and i > 0:# and current[0] != x and current[1] != y:
            path = path[:-1]
            path += "g"
            return path
        if current in visited or (maze[current[0]][current[1]] == water and tree not in tools):
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
        i+=1
    return None

# careful exploring bfs - goes to unknown areas not including crossing water
def careful_exploring_bfs(maze, goal, x, y):
    global tools
    queue = deque([("",(x,y))])
    visited = set()
    graph = special_maze2graph(maze,goal)
    i = 0

    while queue:
        path, current = queue.popleft()
        if maze[current[0]][current[1]] == goal and i > 0:# and current[0] != x and current[1] != y:
            path = path[:-1]
            path += "g"
            return path
        if current in visited or (maze[current[0]][current[1]] == water):
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
        i+=1
    return None

# updates our map with the given 5x5 segment
def update_map(view):
    global my_map, sx, sy, shift_y, shift_x, start, start_pos, prev_pos, tools

    x = sx
    y = sy

    x -= 2
    y -= 2
    
    for i in range(5):
        for j in range(5):
            if i == 2 and j == 2 and my_map[i+x][j+y] != water: 
                my_map[i + x][j + y] = ' '
                continue

            if my_map[i + x][j + y] == "?" :#or (my_map[i + x][j + y] == door and key in tools) or (my_map[i + x][j + y] == tree and axe in tools): 
                my_map[i + x][j + y] = view[i][j]

            if view[i][j] == "O":
                my_map[i + x][j + y] = ' '

    my_map[79][79] = "s"


# helper function for the different bfs's
def solve_view(maze, startX, startY, goal, mode):
   
    if mode == 0:
        path = bfs(maze, goal, startX, startY)
        return path
    elif mode == 1:
        return exploring_bfs(maze, goal, startX, startY)
    elif mode == 2:
        return careful_exploring_bfs(maze, goal, startX, startY)




# decides the action for the AI to make
def get_action(view):

    # update map
    update_map(view)

    global pos

    # start cords
    init_x = 2
    init_y = 2

    # which direction the player is facing
    pos = view[init_x][init_y]

    # solve the map we have constructed from the various 5x5 grid
    
    # solve the given 5x5 grid giving the various tools
    # as the goals, working out way up in the list of most 
    # valuable or whichever is found first
    # usually only one can be found so all other are false 
    # so we go with the true option 

    global my_map, sx, sy

    # special end move for object such as trees and doors 
    end_move = ""

    global shift_x, shift_y, tools

    #print(tools)
    
    # determine which are reachable
    if "$" in tools and solve_view(my_map,sx,sy,"s",0) != None:
        path = solve_view(my_map,sx,sy,"s",0)   
    elif "k" not in tools and solve_view(my_map,sx,sy,"k",0) != None:
        path = solve_view(my_map,sx,sy,"k",0)
        #print(">>>>>>> key")
    elif "k" in tools and solve_view(my_map,sx,sy,"-",0) != None :
        end_move += "UF"
        path = solve_view(my_map,sx,sy,"-",0)
        #print(">>>>>>> door")
    elif "a" not in tools and solve_view(my_map,sx,sy,"a",0) != None :
        path = solve_view(my_map,sx,sy,"a",0)
        #print(">>>>>>> axe")
    elif "a" in tools and solve_view(my_map,sx,sy,"T",0) != None :
        end_move += "CF"
        path = solve_view(my_map,sx,sy,"T",0)
        #print(">>>>>>> tree")
    elif solve_view(my_map,sx,sy,"o",0) != None:
        path = solve_view(my_map,sx,sy,"o",0)
        #print(">>>>>>> stone")
    elif solve_view(my_map,sx,sy,"$",0) != None:
        path = solve_view(my_map,sx,sy,"$",0)
        #print(">>>>>>> prise")
    elif solve_view(my_map,sx,sy,"?",2) != None:
        #print(">>>>>>> careful")
        path = solve_view(my_map,sx,sy,"?",2)
    else:   
        #print(">>>>>>> default  ")
        path = solve_view(my_map,sx,sy,"?",1)        

    global start_pos

    ret = ""
    i,j = sx,sy

    prev_obj = my_map[i][j]
    curr_obj = my_map[i][j]

    for p in path:
        if my_map[i][j] == key or my_map[i][j] == axe or my_map[i][j] == stone or my_map[i][j] == treasure or (my_map[i][j] == tree and axe in tools):
            tools.append(my_map[i][j])
            my_map[i][j] = " "
        if prev_obj == water and curr_obj == " " and stone in tools:
            my_map[prev_x][prev_y] = " "
            tools.remove(stone)
        elif prev_obj == water and curr_obj == " " and tree in tools and stone not in tools:
            tools.remove(tree)
        if prev_obj == " " and curr_obj == water and tree not in tools:
            i = prev_x
            j = prev_y

            ret = ret[:-1]

            if pos == ">":
                ret += "L"
            elif pos == "<":
                ret += "R"
            elif pos == "v":
                ret += "RR"

            pos = "^"
            break

        if p == "g" :
            ret += end_move

            if pos == ">":
                ret += "L"
            elif pos == "<":
                ret += "R"
            elif pos == "v":
                ret += "RR"

            pos = "^"
            break

        if p == "U":
            prev_x = i
            prev_y = j
            
            if pos == "^":
                ret += "F"
            elif pos == ">":
                ret += "LF"
            elif pos == "<":
                ret += "RF"
            elif pos == "v":
                ret += "RRF"

            pos = "^"
            i-=1
        
        elif p == "D":
            prev_x = i
            prev_y = j
        
            if pos == "^":
                ret += "RRF"
            elif pos == ">":
                ret += "RF"
            elif pos == "<":
                ret += "LF"
            elif pos == "v":
                ret += "F"

            pos = "v"

            i+=1
            
        elif p == "L":
            prev_x = i
            prev_y = j
            
            if pos == "^":
                ret += "LF"
            elif pos == ">":
                ret += "RRF"
            elif pos == "<":
                ret += "F"
            elif pos == "v":
                ret += "RF"

            pos = "<"

            j-=1    

        elif p == "R":
            prev_x = i
            prev_y = j
                
            if pos == "^":
                ret += "RF"
            elif pos == ">":
                ret += "F"
            elif pos == "<":
                ret += "LLF"
            elif pos == "v":
                ret += "LF"

            pos = ">"
            
            j+=1

        prev_obj = curr_obj
        curr_obj = my_map[i][j]

    shift_x = i - sx
    shift_y = j - sy
    prev_pos = ret
    
    sx += shift_x
    sy += shift_y

    return ret



# helper function to print the grid
def print_grid(view):
    for ln in view:
        print("|"+str(ln[0])+str(ln[1])+str(ln[2])+str(ln[3])+str(ln[4])+"|")
    print('+-----+')

if __name__ == "__main__":
    # checks for correct amount of arguments 
    if len(sys.argv) != 3:
        print("Usage Python3 "+sys.argv[0]+" -p port \n")
        sys.exit(1)

    port = int(sys.argv[2])

    # checking for valid port number
    if not 1025 <= port <= 65535:
        print('Incorrect port number')
        sys.exit()

    # creates TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
         # tries to connect to host
         # requires host is running before agent
         sock.connect(('localhost',port))
    except (ConnectionRefusedError):
         print('Connection refused, check host is running')
         sys.exit()

    # navigates through grid with input stream of data
    i=0
    j=0
    while 1:
        data=sock.recv(100)
        if not data:
            exit()


        for ch in data:

            if (i==2 and j==2):
                
                view[i][j] = '^'
                view[i][j+1] = chr(ch)
                j+=1 
            else:
                view[i][j] = chr(ch)
            j+=1
            if j>4:
                j=0
                i=(i+1)%5
        if j==0 and i==0:
            #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            #print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            
                        
            action = get_action(view) # gets new actions

            #print(">>>>>>>>>>>"+action)

            sock.send(action.encode('utf-8'))

            time.sleep(0.1)

    sock.close()


