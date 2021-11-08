from enum import Enum
import random
from tkinter.constants import END
import pygame

class CellType(Enum):
    empty = 0
    block = 1
    goal = 2

class Cell():
    def __init__(self, x, y, cellType):
        self.x = x
        self.y = y
        self.cellType = cellType
        self.f = 0
        self.h = 0
        self.g = 0
        self.neighbours = []
        self.walls = []
        self.previous = None
    
    def drawCell(self):
        pygame.draw.rect(window, "#FFFFFF", square(self.x,self.y))
        pygame.display.update()

    def fillCell(self, color):
        pygame.draw.rect(window, color, square(self.x,self.y))
        pygame.time.delay(drawDelay)
        pygame.display.update()

    def getNeighbours(self, cellType):
        x = self.x
        y = self.y
        appendList = None
        if cellType == CellType.empty:
            appendList = self.neighbours
        elif cellType == CellType.block:
            appendList = self.walls
        if self.validNeighboor(x + 1, y, cellType):
            appendList.append(cells[x + 1][y])
        if self.validNeighboor(x, y + 1, cellType):
            appendList.append(cells[x][y + 1])
        if self.validNeighboor(x - 1, y, cellType):
            appendList.append(cells[x - 1][y])
        if self.validNeighboor(x, y - 1, cellType):
            appendList.append(cells[x][y - 1])

    def validNeighboor(self, x, y, cellType):
        if x < 0 or y < 0 or x >= gridSize or y >= gridSize:
            return False
        if cells[x][y].cellType != cellType:
            return False
        return True

def square(x,y):
    return (gridPadding + x*cellSize+1, gridPadding + y*cellSize+1, cellSize-1, cellSize-1)

def heuristic(cell, goal):
    return abs(cell.x - goal.x) + abs(cell.y - goal.y)

def astar (start, goal, h):
    [c.getNeighbours(CellType.empty) for cell in cells for c in cell]

    openSet = {start}
    closedSet = set()
    while len(openSet) > 0:
        lowest = None
        for cell in openSet:
            if not lowest:
                lowest = cell
            elif cell.f < lowest.f:
                lowest = cell
        if lowest == goal:
            return buildPath(lowest)
        openSet.remove(lowest)
        closedSet.add(lowest)
        lowest.fillCell((255,0,0))

        for cell in lowest.neighbours:
            if cell in closedSet:
                continue
            if cell not in openSet:
                cell.g = lowest.g + 1
                cell.h = h(cell, goal)
                cell.f = cell.g + cell.h
                cell.previous = lowest
                openSet.add(cell)
                cell.fillCell((0,255,0))
            elif lowest.g + 1 < cell.g:
                cell.g = lowest.g + 1
                cell.f = cell.g + cell.h
                cell.previous = lowest
    return None
 
def buildPath(current):
    temp = current
    path = [current]
    while temp.previous:
        temp = temp.previous
        path.append(temp)
    path.reverse()
    return path

# def randomBuild():
#     for x in range(gridSize):
#         cells.append([])
#         for y in range(gridSize):
#             if random() * 100 < blockPercent:
#                 cells[x].append(Cell(x, y, CellType.block)) 
#                 cells[x][y].fillCell("#FFFFFF")
#             else:
#                 cells[x].append(Cell(x, y, CellType.empty)) 
#                 cells[x][y].drawCell()
#     start = cells[0][0]
#     goal = cells[gridSize-1][gridSize-1]
#     goal.cellType = CellType.goal
#     return start, goal

def createMaze():
    start = None
    goal = None
    for x in range(gridSize):
        cells.append([])
        for y in range(gridSize):
            if x%2 == 0 and y%2 == 0:
                cells[x].append(Cell(x, y, CellType.empty)) 
                cells[x][y].drawCell()
                if not start:
                    start = cells[x][y]
                else:
                    goal = cells[x][y]
            else:
                cells[x].append(Cell(x, y, CellType.block)) 
    
    start.getNeighbours(CellType.block)
    walls = set(start.walls)
    visited = {start}

    while len(walls) > 0:
        wall = random.choice(tuple(walls))
        walls.remove(wall)
        wall.getNeighbours(CellType.empty)
        for cell in wall.neighbours:
            if cell in visited:
                continue
            wall.cellType = CellType.empty
            wall.drawCell()
            cell.getNeighbours(CellType.block)
            [walls.add(w) for w in cell.walls]
            visited.add(cell)

    return start, goal

gridSize = 100
gridWidth = 700
gridPadding = 20
cellSize = gridWidth/gridSize
blockPercent = 25
drawDelay = 10
cells = []

window = pygame.display.set_mode((gridWidth+gridPadding*2, gridWidth+gridPadding*2))
pygame.init()

start, goal = createMaze()

start.fillCell("#9F2B68")
goal.fillCell("#9F2B68")

path = astar(start, goal, heuristic)

if path:
    [cell.fillCell((0,0,255)) for cell in path]
    print("Success")
else:
    print("Fail")
pygame.time.delay(10000)