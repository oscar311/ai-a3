# !/usr/bin/python3
# ^^ note the python directive on the first line
# COMP 9414 agent initiation file 
# requires the host is running before the agent
# designed for python 3.6
# typical initiation would be (file in working directory, port = 31415)
#        python3 agent.py -p 31415
# created by Leo Hoare
# with slight modifications by Alan Blair

# modified by Oscar Downing (z5114817)

import sys
import socket
import collections
import random
import time
import copy
import numpy as np
from queue import *

# keep track of tools
tools = []

prev_objects = []

# Obstacles  Tools
# T   tree    a   axe
# -   door    k   key
# ~   water   o   stepping stone
# *   wall    $   treasure    

# obstacles
wall, clear, covered = "*", " ", "O"
tree, door, water = "T", "-", "~"

# tools
key, axe, stone, treasure = "k", "a", "o", "$"

# dimensions 
width, height = 5,5

# exploring 2d array
visited = [[" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "]]

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

sx = 40
sy = 40

pos = "^"

start = 1

def update_map(my_map, view):


    #my_map.put(view.copy())

    

    
    global sx, sy
    print(shift_x)
    print(shift_y)

    global start, pos

    if pos == ">":
        np.rot90(view)
        np.rot90(view)
        np.rot90(view)
    elif pos == "v":
        np.rot90(view)
        np.rot90(view)

    elif pos == "<":
        np.rot90(view)



    if shift_x == 0 and shift_y == 0 and start == 1:

        for i in range(0,4):
            for j in range(0,4):
                my_map[sx+i+shift_x][sy+j+shift_y] = view[i][j]

    else:
        start = 2

        for i in range(0,4):
            for j in range(0,4):
                my_map[sx+i+shift_x][sy+j+shift_y] = view[i][j]

        sx+=shift_x
        sy+=shift_y

    for i in range(80) :
        for j in range(80) :
            print(my_map[i][j], end='')
        print()
    

# solve view starts up the recursive solve
# see r_solve()
def solve_view(maze,startX,startY,goal):
    
    # init path array
    p = [[" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "]]

    # init seen array 
    seen = [[False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False]]

    # recursively solve the "maze" solving for different goals
    return r_solve(maze,seen,p,startX,startY,goal)


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
        p[x][y] = "g"
        return x,y, True, p

    if maze[x][y] == wall or maze[x][y] == tree or maze[x][y] == water or maze[x][y] == door or seen[x][y]:
        return x,y, False, p

    seen[x][y] = True

    if x != 0:
        i,j,t, p = r_solve(maze,seen,p,x-1,y,goal) # // Recalls method one to the right
        if t :
            p[x][y] = "U"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
        
            return x,y, t, p
    if x != 4:
        i,j,t, p = r_solve(maze,seen,p,x+1,y,goal) # // Recalls method one to the down
        if t :
            p[x][y] = "D"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
    if y != 0:
        i,j,t, p = r_solve(maze,seen,p,x,y-1,goal) # // Recalls method one to the left
        if t :
            p[x][y] = "L"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
    if y != 4:
        i,j,t, p = r_solve(maze,seen,p,x,y+1,goal) # // Recalls method one to the right
        if t :
            p[x][y] = "R"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return x,y, t, p
            
    return x,y, False, p


# declaring visible grid to agent
view = [[' ' for _ in range(5)] for _ in range(5)]
my_map = [['' for _ in range(80)] for _ in range(80)]

# function to take get action from AI or user
def get_action(view):
    print(tools)
    #print(prev_objects)
    # start cords
    init_x = 2
    init_y = 2

    # which direction the player is facing
    pos = view[init_x][init_y]

    # update the map

    update_map(my_map, view)



    done = False
    while done != True :

        # solve the given 5x5 grid giving the various tools
        # as the goals, working out way up in the list of most 
        # valuable or whichever is found first
        # usually only one can be found so all other are false 
        # so we go with the true option 
        xp, yp, pp, path_p = solve_view(view,init_x,init_y,"$")        
        xk, yk, pk, path_k = solve_view(view,init_x,init_y,"k")
        xa, ya, pa, path_a = solve_view(view,init_x,init_y,"a")
        xo, yo, po, path_o = solve_view(view,init_x,init_y,"o")
        xd, yd, pd, path_d = solve_view(view,init_x,init_y,"-")
        xt, yt, pt, path_t = solve_view(view,init_x,init_y,"T")
        pw = False#xw, yw, pw, path_w = solve_view(view,init_x,init_y,"w")
        xc, yc, pc, path_c = solve_view(view,init_x,init_y,"O")


        # special end move for object such as trees and doors 
        end_move = ""

        # determine which are reachable
        if pp:
            #view[xp][yp] = " "
            path = path_p
            shift_x = xp - init_x
            shift_y = yp - init_y
        elif pk and "k" not in prev_objects:
            #view[xk][yk] = " "
            tools.append("k")
            path = path_k
            shift_x = xk - init_x
            shift_y = yk - init_y
        elif pd and "k" in prev_objects:
            #view[xd][yd] = " "
            end_move += "U"
            path = path_d
            shift_x = xd - init_x
            shift_y = yd - init_y
        elif pa and "a" not in prev_objects:
            #view[xa][ya] = " "
            tools.append("a")
            path = path_a
            shift_x = xa - init_x
            shift_y = ya - init_y
        elif pt and "a" in prev_objects:
            #view[xt][yt] = " "
            end_move += "C"
            path = path_t
            shift_x = xt - init_x
            shift_y = yt - init_y
        elif po:
            #view[xo][yo] = " "
            path = path_o
            shift_x = xo - init_x
            shift_y = yo - init_y
        elif pw and "o" in prev_objects :
            if path_w[xw+1,yw] == "U" :
                if path_w[xw-1][yw] != wall or path_w[xw-1][yw] != water:
                    #view[xw][yw] = " "
                    path = path_w
                    prev_objects.remove("o")
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_w[xw-1][yw] == "D" :
                if path_w[xw+1][yw] != wall or path_w[xw+1][yw] != water:
                    #view[xw][yw] = " "
                    path = path_w
                    prev_objects.remove("o")
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_w[xw][yw+1] == "L": 
                if path_w[xw][yw-1] != wall or path_w[xw][yw-1] != water:
                    #view[xw][yw] = " "
                    path = path_w
                    prev_objects.remove("o")
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_w[xw,yw-1] == "R" :
                if path_w[xw][yw+1] != wall or path_w[xw][yw+1] != water:
                    #view[xw][yw] = " "
                    path = path_w
                    prev_objects.remove("o")
                    shift_x = xw - init_x
                    shift_y = yw - init_y
        elif pc and "O" in prev_objects :
            if path_c[xc+1,yc] == "U" :
                if path_c[xc-1][yc] != wall or path_c[xc-1][yc] != water:
                    #view[xw][yw] = " "
                    path = path_c
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_w[xc-1][yc] == "D" :
                if path_c[xc+1][yc] != wall or path_c[xc+1][yc] != water:
                    #view[xw][yw] = " "
                    path = path_c
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_c[xc][yc+1] == "L": 
                if path_c[xc][yc-1] != wall or path_c[xc][yc-1] != water:
                    #view[xw][yw] = " "
                    path = path_c
                    shift_x = xw - init_x
                    shift_y = yw - init_y
            elif path_w[xc,yc-1] == "R" :
                if path_c[xc][yc+1] != wall or path_c[xc][yc+1] != water:
                    #view[xw][yw] = " "
                    path = path_c
                    shift_x = xw - init_x
                    shift_y = yw - init_y

        # if nothing is reachable we just explore 
        # marking off places we've visited 
        
        else:  

           

            path = [[" ", " ", " ", " ", " "], 
                [" ", " ", " ", " ", " "], 
                [" ", " ", " ", " ", " "], 
                [" ", " ", " ", " ", " "], 
                [" ", " ", " ", " ", " "]]

            i = init_x
            j = init_y
            s = 0

            global search_mode

            attempts = 0

            print(search_mode)

            while i != 0 and i != 4 and j != 0 and j != 4:
                
                if search_mode%8 == left_up and s%2==0:
                    move = "U"
                elif search_mode%8 == left_up and s%2==1:
                    move = "L"
                elif search_mode%8 == right_up and s%2==0:
                    move = "R"
                elif search_mode%8 == right_up and s%2==1:
                    move = "U"
                elif search_mode%8 == left_down and s%2==0:
                    move = "D"
                elif search_mode%8 == left_down and s%2==1:
                    move = "L"
                elif search_mode%8 == right_down and s%2==0:
                    move = "R"
                elif search_mode%8 == right_down and s%2==1:
                    move = "D"

                elif search_mode%8 == left:
                    move = "L"
                elif search_mode%8 == right:
                    move = "R"
                elif search_mode%8 == up:
                    move = "U"
                elif search_mode%8 == down:
                    move = "D"




                if move == "U" and path[i-1][j] == clear and  view[i-1][j] != wall and view[i-1][j] != water:

                    path[i][j] = "U"
                    path[i-1][j] = "g"
                    i-=1
                elif move == "D" and path[i+1][j] == clear and view[i+1][j] != wall and view[i+1][j] != water:
                    path[i][j] = "D"
                    path[i+1][j] = "g"
                    i+=1
                elif move == "L" and path[i][j-1] == clear and view[i][j-1] != wall and view[i][j-1] != water :
                    path[i][j] = "L"
                    path[i][j-1] = "g"
                    j-=1
                elif move =="R" and path[i][j+1] == clear and view[i][j+1] != wall and view[i][j+1] != water:
                    path[i][j] = "R"
                    path[i][j+1] = "g"
                    j+=1
                else :
                    search_mode+=1
                if attempts > 6400:
                    path = [[" ", " ", " ", " ", " "], 
                        [" ", " ", " ", " ", " "], 
                        [" ", " ", " ", " ", " "], 
                        [" ", " ", " ", " ", " "], 
                        [" ", " ", " ", " ", " "]]

                    i = init_x
                    j = init_y
                    s = 0

                attempts+=1
                    
                s+=1
            
            global shift_x, shift_y

            shift_x = i - init_x
            shift_y = j - init_y

            search_mode+=1
 


        ret = ""
        i,j = 2,2
        while path[i][j] != "g" :

            if view[i][j] == water:
                break 

            if path[i][j] == "U":

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

            elif path[i][j] == "D":

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

            elif path[i][j] == "L":

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

            elif path[i][j] == "R":

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
            

        ret += end_move



        break
    time.sleep(.1)
    print(ret)
    return ret


# helper function to print the grid
def print_grid(view):
    print('+-----+')
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

            if i == 1 and j == 2 and ch != wall and ch != water and ch != door and ch != tree and ch != clear:
                prev_objects.append(chr(ch))

            if (i==2 and j==2):
                
                view[i][j] = '^'
                view[i][j+1] = chr(ch)
                j+=1 
            else:
                #prev_objects.append(ch)

                view[i][j] = chr(ch)
            j+=1
            if j>4:
                j=0
                i=(i+1)%5
        if j==0 and i==0:
            print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            action = get_action(view) # gets new actions
            sock.send(action.encode('utf-8'))

    sock.close()