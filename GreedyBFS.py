import sys
from collections import deque

class Node:
    def __init__(self,state,parent,action,end):
        self.state = state
        self.parent  = parent
        self.action  = action
        self.end = end
        self.manhattan = self.manhattanDistance()
        
    def manhattanDistance(self):
        dist = 0
        for i in range(len(self.state)):
            dist += abs(self.state[i] - self.end[i])
        return dist
        

class QueueFrontier():
    def __init__(self):
        self.frontier = deque()

    def add(self,node):
        self.frontier.appendleft(node)
    
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            less = 0
            for i in range(len(self.frontier)):
                if self.frontier[i].manhattan < self.frontier[less].manhattan:
                    less = i
            node = self.frontier[less]
            del self.frontier[less]
            return node

class Maze:
    def __init__(self,filename):

        with open(filename) as f:
            contents =  f.read()
        
        # check if starting point is existing or not

        if contents.count("A") != 1:
            print("Error : No starting point")
            return
        if contents.count("B") != 1:
            print("Error : No final point ")
            return

        contents = contents.splitlines()
        # get the width and height
        self.height = len(contents)
        self.width = max([len(row) for row in contents])
    
        self.walls = []
        
        for row in range(self.height):
            line = []
            for col in range(self.width):
                if contents[row][col] == "A":
                    self.start = (row,col)
                    line.append(True)
                elif contents[row][col] == "B":
                    self.end = (row,col)
                    line.append(True)
                elif contents[row][col] == " ":
                    line.append(True)
                else:
                    line.append(False)
            self.walls.append(line)
        self.solution = None

    def neighbors(self,state):
        row , col = state
        movement = [
            ("up",(row - 1, col)),
            ("down",(row + 1, col)),
            ("left",(row, col - 1)),
            ("right",(row, col + 1)),
        ]
        
        # get result
        result = []
        for action , (r,c) in movement:
            if 0 <= r < self.height and 0 <= c < self.width and self.walls[r][c]:
                result.append((action,(r,c)))
        return result
    def print(self):
        solution = self.solution[1] if self.solution else None
        # print(solution)  
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
               
                if not col:
                    print("☒",end=" ")
                elif (i,j) == self.start:
                    print("A",end=" ")
                elif (i,j) == self.end:
                    print("B",end=" ")
                elif solution is not None and (i,j) in solution:
                    print("*",end=" ")
                else:
                    print(" ",end=" ")
              
            print()
        print()
    def solved(self):

        self.num_explored = 0
        # initial value or initial state
        start = Node(state=self.start,parent=None,action=None,end=self.end)
        frontier = QueueFrontier()
        frontier.add(start)
        
        # checker kung ano na yung mga naexplore natin
        self.explored = set()

        while True:
            
            # check if it is empty
            if frontier.empty():
                print("Error : No Solution")
                return

            # remove the lowest manhattan distance
            node = frontier.remove()
            # increment the explored number
            self.num_explored += 1
            

            if node.state == self.end:
                # meaning tapos na 
                action = []
                coordinate = [] 
                while node.parent is not None:
                    action.append(node.action)
                    coordinate.append(node.state)
                    node = node.parent
                self.solution = (action,coordinate)
                return 
            
            # add the coordinate in the explored set 
            self.explored.add(node.state)

            # lets check the neighbor 
            for action,state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state,parent=node,action=action,end=self.end)
                    frontier.add(child)
              


a = Maze("maze1.txt")
# print(a.contents)
# print(a.width)
# print(a.walls)
a.solved()
print("State Explore :",a.num_explored)
a.print()