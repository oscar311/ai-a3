#!/usr/bin/python3

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

# The data structure used to keep track of all the known parts of the map is a 160 x 160 2D array. This size is to accommodate an 80 x 80 map which starts the agent in the corner.
# In our data structure the agent starts in the middle so whichever way the map grows it will never go past the edge of the array.

# Each time a new map segment is received, the map data structure is updated with the new information.
# A Breadth first search is then performed on all of the objects

# If a path to the treasure cannot be found, the agent is insutructed to move around and discover more of the map.

# This is repeated until a path can be found to the treasure and all the tools required.

# Finally a path is constructed to aquire all the tools necessary and to the treasure then back to the start.

import sys
import socket
import collections
import random
import time
import copy
import numpy as np
from   collections import deque


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

# dimensions 
width, height = 5,5


# previous x and y of player
shift_x = 0
shift_y = 0

search_mode = 0

left_up = 2
left_down = 3
right_up = 0
right_down = 1
left = 4
right = 5
up = 6
down = 7
 #= Queue(maxsize=1000)

sx = 39
sy = 39

pos = "^"
start_pos = "^"


start = 1

prev_pos = ""

rot = 0

# declaring visible grid to agent
view = [['' for _ in range(5)] for _ in range(5)]
#my_map = [['' for _ in range(80)] for _ in range(80)]

my_map = np.array([['?' for _ in range(80)] for _ in range(80)])


visited = set()
def special_maze2graph(maze):
    global tools
    height = 80
    width = 80
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == wall}

    if key in tools and axe in tools:
    
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge :#and not maze[row + 1][col] == tree and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge :#and not maze[row][col + 1] == tree and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))

    elif key in tools:
        for row, col in graph.keys():


            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == tree:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == tree:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    elif axe in tools:
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    else :
        print("herro")
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == tree and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == tree and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))


    
    ##print(graph)
        
    return graph


def maze2graph(maze):
    global tools
    height = 80
    width = 80
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j] == wall}

    if key in tools and axe in tools:
    
        for row, col in graph.keys():
            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == "?" :#and not maze[row + 1][col] == tree and not maze[row + 1][col] == door:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == "?" :#and not maze[row][col + 1] == tree and not maze[row][col + 1] == door:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))

    elif key in tools:
        for row, col in graph.keys():


            if row < height - 1 and not maze[row + 1][col] == wall and not maze[row + 1][col] == edge and not maze[row + 1][col] == "?" and not maze[row + 1][col] == tree:
                graph[(row, col)].append(("D", (row + 1, col)))
                graph[(row + 1, col)].append(("U", (row, col)))
            if col < width - 1 and not maze[row][col + 1] == wall and not maze[row][col + 1] == edge and not maze[row][col + 1] == "?" and not maze[row][col + 1] == tree:
                graph[(row, col)].append(("R", (row, col + 1)))
                graph[(row, col + 1)].append(("L", (row, col)))
    elif axe in tools:
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


    
    ##print(graph)
        
    return graph


def bfs(maze, goal, x, y):
    global tools
    queue = deque([("",(x,y))])
    visited = set()
    graph = maze2graph(maze)
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


def global_bfs(maze, goal, x, y):
    global tools
    queue = deque([("",(x,y))])
    visited = set()
    graph = special_maze2graph(maze)
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



def update_map(view):


    #my_map.put(view.copy())
    
    global my_map, sx, sy, shift_y, shift_x
    ##print(shift_x)
    ##print(shift_y)
    ##print(sx)
    ##print(sy)


    

    #print_grid(prev_view)
    global start, start_pos, prev_pos, tools

    ##print(">>> prev pos " + prev_pos)


    #global rot

    """if rot != 0:
        my_map = np.rot90(my_map,-rot)
    """
    

    #rot = 0
    for i in prev_pos:
        if i == "L":
            view = np.rot90(view,1)
            #rot+=1
        elif i == "R":
            view = np.rot90(view,3)
            #rot-=1

    

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


    """

    if shift_x == 0 and shift_y == 0 and start == 1:

        for i in range(5):
            for j in range(5):
                if my_map[sx+i+shift_x][sy+j+shift_y] == "" or my_map[sx+i+shift_x][sy+i+shift_y] == " ":

                    my_map[sx+i+shift_x][sy+j+shift_y] = view[i][j]

    else:
        start = 2

        for i in range(5):
            for j in range(5):
                if my_map[sx+i+shift_x][sy+i+shift_y] == "" or my_map[sx+i+shift_x][sy+i+shift_y] == " ":

                    my_map[sx+i+shift_x][sy+j+shift_y] = view[i][j]

        sx+=shift_x
        sy+=shift_y
    """

    my_map[39][39] = "s"
    """
    for i in prev_pos:
        if i == "L":
            my_map = np.rot90(my_map,-1)
            #rot+=1
        elif i == "R":
            my_map = np.rot90(my_map,1)
            #rot-=1
    """
    
    to_print = np.rot90(my_map,3)
    for i in range(80) :
        for j in range(80) :
            print(to_print[i][j], end='')
        print()
    






# solve view starts up the recursive solve
# see r_solve()
def solve_view(maze,startX,startY,goal, mode):
    
    # init path array
    p = ""
    seen = np.array([[False for _ in range(80)] for _ in range(80)])

    

    if mode == 0:
        path = bfs(maze, goal, startX, startY)
        return path
    elif mode == 1:
        # recursively solve the "maze" solving for different goals
        #return r_solve(maze,seen,p,startX,startY,goal, startX, startY)
        return global_bfs(maze, goal, startX, startY)

# recursive function that solves the maze, given a goal
#   - maze = given puzzle to solve
#   - seen = the closed node 2d array
#   - p = path
#   - x,y = x start cord, y start cord
#   - goal = where to end
#   
# returns
#   - x, y = x end cord, y end cord
#   - False = whether or not the maze was solvable
#   - p = the path 
def r_solve(maze,seen,p,x,y,goal):
    
    if maze[x][y] == goal: 
        p += "g"
        return x,y, True, p

    if maze[x][y] == "?" or maze[x][y] == wall or maze[x][y] == tree or maze[x][y] == water or maze[x][y] == door or seen[x][y]:
        return x,y, False, p

    seen[x][y] = True

    if x != 0:
        i,j,t, p = r_solve(maze,seen,p,x-1,y,goal, startX, startY) # // Recalls method one to the right
        if t :
            p += "U"; #// Sets that path value to true;
            ##print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
        
            return x,y, t, p
    if x != 79:
        i,j,t, p = r_solve(maze,seen,p,x+1,y,goal, startX, startY) # // Recalls method one to the down
        if t :
            p += "D"; #// Sets that path value to true;
            ##print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
    if y != 0:
        i,j,t, p = r_solve(maze,seen,p,x,y-1,goal, startX, startY) # // Recalls method one to the left
        if t :
            p += "L"; #// Sets that path value to true;
            ##print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
    if y != 79:
        i,j,t, p = r_solve(maze,seen,p,x,y+1,goal, startX, startY) # // Recalls method one to the right
        if t :
            p += "R"; #// Sets that path value to true;
            ##print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
            
    return x,y, False, p



# function to take get action from AI or user
def get_action(view):
    ##print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    global pos, prev_pos
    ##print("prev pos" + prev_pos)
    #print_grid(view)

    #update_map()

    ##print(prev_objects)
    # start cords
    init_x = 2
    init_y = 2

    

    # which direction the player is facing
    pos = view[init_x][init_y]

    # update the map



    # solve the given 5x5 grid giving the various tools
    # as the goals, working out way up in the list of most 
    # valuable or whichever is found first
    # usually only one can be found so all other are false 
    # so we go with the true option 

    global my_map, sx, sy

    
    #path_w = None#xw, yw, pw, path_w = solve_view(view,sx,sy,"w")
    #path_c = solve_view(my_map,sx,sy,"O",0) 


    # special end move for object such as trees and doors 
    end_move = ""

    global shift_x, shift_y, tools

    print(tools)
    

    #global visited
    # determine which are reachable
    if "$" in tools and solve_view(my_map,sx,sy,"s",0) != None:
        path = solve_view(my_map,sx,sy,"s",0)   
    elif "k" not in tools and solve_view(my_map,sx,sy,"k",0) != None:
        #view[xk][yk] = " "
        #tools.append("k")
        path = solve_view(my_map,sx,sy,"k",0)
        #print(">>>>>>> key")
        #visited = set()
        #shift_x = xk - init_x
        #shift_y = yk - init_y
    elif "k" in tools and solve_view(my_map,sx,sy,"-",0) != None :
        #view[xd][yd] = " "
        end_move += "UF"
        path = solve_view(my_map,sx,sy,"-",0)
        #print(">>>>>>> door")
        #visited = set()
        #shift_x = xd - init_x
        #shift_y = yd - init_y
    elif "a" not in tools and solve_view(my_map,sx,sy,"a",0) != None :
        #view[xa][ya] = " "
        #tools.append("a")
        path = solve_view(my_map,sx,sy,"a",0)
        #print(">>>>>>> axe")
        #visited = set()
        #shift_x = xa - init_x
        #shift_y = ya - init_y
    elif "a" in tools and solve_view(my_map,sx,sy,"T",0) != None :
        #view[xt][yt] = " "
        end_move += "CF"
        path = solve_view(my_map,sx,sy,"T",0)
        #print(">>>>>>> tree")
        #visited = set()
        #shift_x = xt - init_x
        #shift_y = yt - init_y
    elif solve_view(my_map,sx,sy,"o",0) != None:
        #view[xo][yo] = " "
        path = solve_view(my_map,sx,sy,"o",0)
        #print(">>>>>>> stone")

        #visited = set()
        #shift_x = xo - init_x
        #shift_y = yo - init_y
    elif solve_view(my_map,sx,sy,"$",0) != None:
        #view[xp][yp] = " "
        path = solve_view(my_map,sx,sy,"$",0)
        #tools.append("$")
        #print(">>>>>>> prise")
        #visited = set()
        #shift_x = xp - init_x
        #shift_y = yp - init_y  
    else:   
        
        path = solve_view(my_map,sx,sy,"?",1)        


        #print(">>>>>>>>>>>>>>>> basic")
        """path = ""

        i = sx
        j = sy
        

        while i != 0 and i != 79 and j != 0 and j != 79:

            s = random.choice(["U","D","L","R"])

            if s == "D" and my_map[i+1][j] != "?" and my_map[i+1][j] != wall and my_map[i+1][j] != water:
                path += "D"
                i+=1
            elif s == "U" and my_map[i-1][j] != "?" and my_map[i-1][j] != wall and my_map[i-1][j] != water:
                path += "U"
                i-=1
            elif s == "L" and my_map[i][j-1] != "?" and my_map[i][j-1] != wall and my_map[i][j-1] != water :
                path += "L"
                j-=1
            elif s == "R" and my_map[i][j+1] != "?" and my_map[i][j+1] != wall and my_map[i][j+1] != water:
                path += "R"
                j+=1
            else :
                break

        path += "g"
        """
    global start_pos

    ret = ""
    i,j = sx,sy

    """
    if pos == ">":
        ret += "L"
    elif pos == "<":
        ret += "R"
    elif pos == "v":
        ret += "RR"""
    prev_obj = my_map[i][j]
    curr_obj = my_map[i][j]
    for p in path:

        #print(my_map[i][j], end=',')

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

            #print("herro")

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

        #if my_map[i][j] == water:
        #    break 

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

        ##been_here[i][j] = True
    #print()
    #print(sx)
    #print(sy)
    print(i)
    print(j)


    #prev_view = view[:]
    #print_grid(path)
    shift_x = i - sx
    shift_y = j - sy
    prev_pos = ret
    

    
    sx += shift_x
    sy += shift_y


    print(path)
    print(ret)
    return ret


# helper function to print the grid
def print_grid(view):
    #print('+-----+')
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
        #print('Incorrect port number')
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
            print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            
            update_map(view)            
            action = get_action(view) # gets new actions

            #print(">>>>>>>>>>>"+action)

            sock.send(action.encode('utf-8'))

            time.sleep(0.5)

    sock.close()