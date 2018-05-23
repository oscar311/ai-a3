#!/usr/bin/python3
# ^^ note the python directive on the first line
# COMP 9414 agent initiation file 
# requires the host is running before the agent
# designed for python 3.6
# typical initiation would be (file in working directory, port = 31415)
#        python3 agent.py -p 31415
# created by Leo Hoare
# with slight modifications by Alan Blair

import sys
import socket
import collections
import random
import time
"""
def bfs(grid, start, goal, tools):

    width, height = 5,5

    wall, clear = "*", " "

    tree, door, water = "T", "-", "~"

    # Obstacles  Tools
    # T   tree    a   axe
    # -   door    k   key
    # ~   water   o   stepping stone
    # *   wall    $   treasure    

    #take the first element 
    queue = collections.deque([[start]])
    seen = set([start])
    
    while queue:
        path = queue.popleft()
        x, y = path[-1]

        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[x2][y2] != wall and (x2, y2) not in seen:
                
                if grid[x2][y2] == water and "o" in tools or grid[x2][y2] == door and "k" in tools or grid[x2][y2] == tree and "a" in tools or grid[x2][y2] == clear :
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))

            if 0 <= x2 < width and 0 <= y2 < height and grid[x2][y2] == wall and (x2, y2) not in seen:
                for i in range(0, 5):
                    if grid[x2+i] == "*":
                        
                        break;
                    elif grid[x2-i] == "*":
                        break;
                    elif grid[y2-i] == "*":
                        break;
                    elif grid[y2-i] == "*":
                        break;
"""
"""
int[][] maze = new int[width][height]; // The maze
boolean[][] wasHere = new boolean[width][height];
boolean[][] p = new boolean[width][height]; // The solution to the maze
int startX, startY; // Starting X and Y values of maze
int endX, endY;     // Ending X and Y values of maze
"""



def solve_maze(maze,startX,startY,goal,tools):
    
    width, height = 5,5

    # Obstacles  Tools
    # T   tree    a   axe
    # -   door    k   key
    # ~   water   o   stepping stone
    # *   wall    $   treasure    

    #take the first element 

    p = [[" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "], 
        [" ", " ", " ", " ", " "]]

    seen = [[False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False], 
            [False, False, False, False, False]]


    t, path = r_solve(maze,seen,p,startX,startY,goal,tools)
    return t,path


def r_solve(maze,seen,p,x,y,goal,tools):
    
    wall, clear = "*", " "

    tree, door, water = "T", "-", "~"


    if maze[x][y] == goal: 
        #print("goal >>>> " + str(x) + " " + str(y) + " <<<<<") 
        p[x][y] = "g"
        return True, p

    """if maze[x][y] == tree and "a" in tools:
        p[x][y] = True
        return True, p
    if maze[x][y] == water and "o" in tools:
        p[x][y] = True
        return True, p
    if maze[x][y] == door and "k" in tools:
        p[x][y] = True
        return True, p
    """
    if maze[x][y] == wall or maze[x][y] == tree or maze[x][y] == water or maze[x][y] == door or seen[x][y]:
        #print("obstacle >>>> " + str(x) + " " + str(y) + " <<<<<") 
        
        return False, p

    seen[x][y] = True


    if x != 0:
        t, p = r_solve(maze,seen,p,x-1,y,goal,tools) # // Recalls method one to the left
        if t :
            p[x][y] = "U"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
        
            return t, p
    if x != 4:
        t, p = r_solve(maze,seen,p,x+1,y,goal,tools) # // Recalls method one to the left
        if t :
            p[x][y] = "D"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return t, p
    if y != 0:
        t, p = r_solve(maze,seen,p,x,y-1,goal,tools) # // Recalls method one to the left
        if t :
            p[x][y] = "L"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return t, p
    if y != 4:
        t, p = r_solve(maze,seen,p,x,y+1,goal,tools) # // Recalls method one to the left
        if t :
            p[x][y] = "R"; #// Sets that path value to true;
            #print(">>>> " + str(x) + " " + str(y) + " <<<<<") 
            
            return t, p
            
    return False, p


# declaring visible grid to agent
view = [['' for _ in range(5)] for _ in range(5)]

# function to take get action from AI or user
def get_action(view):

    ## REPLACE THIS WITH AI CODE TO CHOOSE ACTION ##


    # Obstacles  Tools
    # T   tree    a   axe
    # -   door    k   key
    # ~   water   o   stepping stone
    # *   wall    $   treasure

    x = 2
    y = 2

    tools = []

    pos = view[2][2]

    done = False
    while done != True :



        pp, path_p = solve_maze(view,x,y,"$", tools)        
        pk, path_k = solve_maze(view,x,y,"k", tools)
        pa, path_a = solve_maze(view,x,y,"a", tools)
        po, path_o = solve_maze(view,x,y,"o", tools)
        pd, path_d = solve_maze(view,x,y,"-", tools)


        """
        m = ["U","D","L","R"]
        p = [m[random.randint(0,3)], m[random.randint(0,3)], m[random.randint(0,3)], m[random.randint(0,3)]]
        """

        end_move = ""

        if pp:

            path = path_p
        elif pk:
            
            path = path_k
        elif pd:
            end_move += "U"
            path = path_d
        elif pa:

            path = path_a
        elif po:
            path = path_o
        else:  

            i = random.randint(0,3)

            path1 = [[" ", " ", " ", " ", " "], 
                    [" ", " ", " ", " ", " "], 
                    [" ", " ", "D", " ", " "], 
                    [" ", " ", "R", "D", " "], 
                    [" ", " ", " ", "R", "g"]]

            path2 = [[" ", " ", " ", "R", "g"], 
                    [" ", " ", "R", "U", " "], 
                    [" ", " ", "U", " ", " "], 
                    [" ", " ", " ", " ", " "], 
                    [" ", " ", " ", " ", " "]]


            path3 = [["g", "L", " ", " ", " "], 
                    [" ", "U", "L", " ", " "], 
                    [" ", " ", "U", " ", " "], 
                    [" ", " ", " ", " ", " "], 
                    [" ", " ", " ", " ", " "]]


            path4 = [[" ", " ", " ", " ", " "], 
                    [" ", " ", " ", " ", " "], 
                    [" ", " ", "D", " ", " "], 
                    [" ", " ", "D", " ", " "], 
                    ["g", "L", "L", " ", " "]]
        
            u = [path1,path2,path3,path4]
            path = u[i]

        ret = ""

        print(path)

        
        i,j = 2,2

        while path[i][j] != "g":
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
        print("Usage python3 "+sys.argv[0]+" -p port \n")
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
            print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            action = get_action(view) # gets new actions
            sock.send(action.encode('utf-8'))

    sock.close()
