# gridlate PY file to get started with CENG462-HW1
# do not forget to rename the file before you submit it
import numpy as np
from copy import deepcopy
# you can import the related data structures from the package queue
# have fun!
# -mferhata

def astar(problem):
    depth = 0
    frontierList = []
    exploredList = []
    frontierList.append(problem)
    while (frontierList ):

        bestMove, bestIndex = getBest(frontierList)
        depth += 1
        if not np.any(bestMove.grid == 2):

            # print(depth)
            # print("SUCCESS")
            return bestMove
        frontierList.pop(bestIndex)
        exploredList.append(bestMove)
        moveList = []
        tile = bestMove.move_right()
        if type(tile)!=problem:
            moveList.append(tile)
        tile = bestMove.move_left()
        if type(tile)!=problem:
            moveList.append(tile)
        tile = bestMove.climb_right()
        if type(tile)!=problem:
            moveList.append(tile)
        tile = bestMove.climb_left()
        if type(tile)!=problem:
            moveList.append(tile)
        # print(moveList)
        for move in moveList:
            flag = False
            for explored in exploredList:
                if np.array_equal(explored.grid , move):
                    flag = True
                    break
            if (flag == False):
                cost = bestMove.gVal + 1
                current = False
                for frontier in frontierList:

                    if (frontier == move):
                        bestIndex = frontierList.index(frontier)
                        current = True
                        if (cost < frontierList[bestIndex].gVal):
                            frontierList[bestIndex].gVal = cost
                            # print("asd")
                            frontierList[bestIndex].parent = bestMove
                if (current == False and move!=[] ):
                    # print("asd")
                    move.gVal = cost
                    move.hVal = move.compute_h(np.where(move.grid == 2),np.where(move.grid == 4),move.grid)
                    move.fVal = move.gVal + move.hVal + move.hVal
                    frontierList.append(move)
    # print(depth)
    return None

def idastar(problem):
    print('IDA*')
    # TODO implement IDA* to solve the problem
    # > you can take 200 as the upper bound on 'depth'

def getBest(frontierList):
    fVal = float("inf")
    bestIndex = 0
    for index, i in enumerate(frontierList):
        if (i.fVal < fVal):
            fVal = i.fVal
            bestIndex = index

    return frontierList[bestIndex], bestIndex
class Problem:
    # 0: Empty cell
    # 1: Wall
    # 2: Agent
    # 3: Rock
    # 4: Gate
    def __init__(self):
        self.height = 6
        self.blocking_objs= [1, 3]
        self.falling_objs = [3, 2, 4]
        self.gVal = 0
        self.hVal = 0
        self.fVal = 0
    def compute_h(self,agent_pos, gate_pos, board):
        agent_row,agent_col=agent_pos
        gate_row, gate_col = gate_pos

        dist = 0
        if not np.any(board == 2):
            return dist
        for col in range(agent_col[0], gate_col[0] ):
            if len(np.where((board[:, col] == 1))[0]) >len(np.where((board[:, col + 1] == 1))[0]):
                dist+=1
            else:
                dist+= len(np.where((board[:, col + 1] == 1))[0]) - len(np.where((board[:, col] == 1))[0]) - 1
        return dist


    def move_right(self):
        p2 =  deepcopy(self)
        if not np.any(p2.grid == 2):
            return []
        row, col = np.where(p2.grid == 2)
        if col >= self.width - 1 or (p2.grid[row, col + 1] == 1) :
            return []
        elif p2.grid[row , col + 1] == 4:
            p2.grid[row, col ]=0
        elif (p2.grid[row, col + 1] == 0 ):
            p2.grid[row , col + 1] = 2
            p2.grid[row, col] = 0
        elif p2.grid[row, col + 1] == 3:
            if (p2.grid[row +1, col + 1] in [1, 3, 4] ):
                return []
            else:
                if row +2 > self.width :
                    pass
                elif  p2.grid[row , col + 2] == 0:
                    p2.grid[row , col + 2] = 3
                    p2.grid[row , col + 1] = 2
                    p2.grid[row, col] = 0
                elif p2.grid[row , col + 2] == 4:
                    p2.grid[row, col + 1] = 2
                    p2.grid[row, col] = 0
                elif p2.grid[row , col + 2] in self.blocking_objs and p2.grid[row +1, col + 2]==0:
                    p2.grid[row+1, col + 2] = 3
                    p2.grid[row, col + 1] = 2
                    p2.grid[row, col] = 0
                elif p2.grid[row, col + 2] in self.blocking_objs and p2.grid[row + 1, col + 2] == 4:

                    p2.grid[row, col + 1] = 2
                    p2.grid[row, col] = 0

        self.free_fall()
        return p2
    def move_left(self):
        p2 = deepcopy(self)
        if not np.any(p2.grid == 2):
            return []
        row, col = np.where(p2.grid == 2)
        if col-1 <= 0 or (p2.grid[row, col - 1] == 1) :
            return []
        elif p2.grid[row , col -1] == 4:
            p2.grid[row, col ]=0
        elif (p2.grid[row, col - 1] == 0 ):
            p2.grid[row , col - 1] = 2
            p2.grid[row, col] = 0
        elif p2.grid[row, col - 1] == 3:
            if (p2.grid[row +1, col - 1] in [1, 3, 4] ):
                return []
            else:
                if col -2 < 0   :
                    pass
                elif  p2.grid[row , col - 2] == 0:
                    p2.grid[row , col - 2] = 3
                    p2.grid[row , col - 1] = 2
                    p2.grid[row, col] = 0
                elif p2.grid[row , col - 2] in p2.blocking_objs and p2.grid[row +1, col - 2]==0:
                    p2.grid[row+1, col - 2] = 3
                    p2.grid[row, col - 1] = 2
                    p2.grid[row, col] = 0
                elif p2.grid[row, col -2] in self.blocking_objs and p2.grid[row + 1, col -2] == 4:

                    p2.grid[row, col - 1] = 2
                    p2.grid[row, col] = 0

        p2.free_fall()
        return p2
    def climb_right(self):
        p2 = deepcopy(self)
        if not np.any(p2.grid == 2):
            return []
        row, col = np.where(p2.grid == 2)
        if col < p2.width - 1 and (p2.grid[row, col + 1] == 0 or p2.grid[row, col + 1] == 4):
            return []
        elif col < p2.width - 1 and p2.grid[row, col + 1] in [1, 3]:
            if row > 0 and (p2.grid[row +1, col + 1] == 0):
                p2.grid[row + 1, col + 1] = 2
                p2.grid[row, col] = 0
            elif p2.grid[row +1, col + 1] == 4:
                p2.grid[row, col] = 0
            elif row > 0 and p2.grid[row + 1, col + 1] == 1:
                return []
            elif row > 0 and p2.grid[row + 1, col + 1] == 3:
                if row > 1 and p2.grid[row + 2, col + 1] == 3 or p2.grid[row + 2, col + 1] in self.blocking_objs:
                    return []
                elif col < p2.width + 2 and p2.grid[row + 1, col + 2] == 0:

                    p2.grid[row + 1, col + 2] = 3
                    p2.grid[row + 1, col + 1] = 2
                    p2.grid[row, col] = 0
                elif col < p2.width + 2 and p2.grid[row + 1, col + 2] == 4:
                    p2.grid[row + 1, col + 1] = 2
                    p2.grid[row, col] = 0
                else:
                    return []
        p2.free_fall()
        return p2

    def climb_left(self):

        p2 = deepcopy(self)
        if not np.any(p2.grid == 2):
            return []
        row, col = np.where(p2.grid == 2)

        if col > 0 and (p2.grid[row, col -1] == 0 or p2.grid[row, col-1] == 4):
            return []
        elif col > 0 and p2.grid[row, col - 1] in [1, 3]:
            if row > 0 and (p2.grid[row +1, col - 1] == 0 or p2.grid[row +1, col - 1] == 4):
                p2.grid[row + 1, col - 1] = 2
                p2.grid[row, col] = 0
            elif p2.grid[row +1, col - 1] == 4:
                p2.grid[row, col] = 0
            elif row > 0 and p2.grid[row + 1, col - 1] == 1:
                return []
            elif row > 0 and p2.grid[row + 1, col - 1] == 3:
                if row > 1 and p2.grid[row + 2, col - 1] == 3 or p2.grid[row - 2, col - 1] == 5:
                    return []
                elif col > 1 and p2.grid[row + 1, col - 2] == 0:
                    p2.grid[row + 1, col - 2] = 3
                    p2.grid[row + 1, col - 1] = p2.grid[row, col]
                    p2.grid[row, col] = 0
                elif col < p2.width + 2 and p2.grid[row + 1, col - 2] == 4:
                    p2.grid[row + 1, col - 1] = 2
                    p2.grid[row, col] = 0
                else:
                    return []
        p2.free_fall()
        return p2
    def free_fall(self):
        p2 = deepcopy(self)
        for obj in self.falling_objs:
            rows,cols = np.where(self.grid==obj)
            for row, col in zip(rows, cols):
                while row > 0 and (self.grid[row - 1, col] == 0 or self.grid[row - 1, col] == obj):
                    if self.grid[row - 1, col] == 0:
                        self.grid[row - 1, col] = obj
                        self.grid[row, col] = 0
                    elif self.grid[row - 1, col] == 4 and obj == 3:
                        self.grid[row, col] = 0
                    row -= 1
    def init_from_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        if lines[0].split()[0] == 'A*':
            self.solver = astar
        else:
            self.solver = idastar

        state = ''
        for line in lines[1:]:
            strings = line.split()
            if strings[0] == 'W':
                # number of specif
                # ied wall-heights decide the grid's width
                self.width  = len(strings) - 1
                self.grid   = np.zeros((self.height,self.width))
                for col,string in enumerate(strings[1:]):
                    # height is always a nonnegative number
                    height  = int(string)
                    self.grid[height::-1,col] = 1
            else:
                state += strings[0] + ','
                for string in strings[1:]:
                    state += string.zfill(2) + ','
        self.starting_state = state[:-1]
        self.set_from_state(state)

    # a STATE encoding looks like: "R,02,02,A,01,G,09"
    # STATE should start with 'R,'
    # ofc, you are free to change this convention
    def set_from_state(self, state):
        self.grid = np.where(self.grid<2, self.grid, np.zeros(self.grid.shape))

        reading = ''
        for string in state.split(','):
            if string in 'ARG':
                reading = string
            else:
                col = int(string)
                # place the object on top
                self.grid[self.height-1,col] = 'ARG'.index(reading) + 2
                # let it fall
                self.free_fall()
    
    def pretty_print(self):
        print('=='*(self.width+2))
        for row in self.grid[self.height-1::-1,:]:
            print('||', end='')
            for val in row:
                to_disp = ' WARG'[int(val)] + ' '
                print(to_disp, end='')
            print('||')
        print('=='*(self.width+2))

filename = input()
p = Problem()
p.init_from_file(filename)
p.pretty_print()
p=astar(p)
