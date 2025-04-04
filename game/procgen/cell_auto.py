import random
import numpy as np
from typing import List
from math import sqrt
from game.core import tile_types
from game.core.game_map import GameMap

class CellularAutomata:
    '''
    Rather than implement a traditional cellular automata, I
    decided to try my hand at a method discribed by "Evil
    Scientist" Andy Stobirski that I recently learned about
    on the Grid Sage Games blog.
    '''
    def __init__(self):
        self.level = []
        self.iterations = 30000
        self.neighbours = 4 # number of neighboring walls for this cell to become a wall
        self.wallProbability = 0.50 # the initial probability of a cell becoming a wall, recommended to be between .30 and .55

        self.ROOM_MIN_SIZE = 10 # size in total number of cells
        self.ROOM_MAX_SIZE = 20

        self.smoothEdges = True
        self.smoothing = 1

    def generate_dungeon(self, map_width: int, map_height: int) -> GameMap:
        dungeon = GameMap(map_width, map_height)

        self.caves = []

        self.level = dungeon.tiles

        self.level[0:map_width, 0:map_height] = tile_types.wall

        self.randomFillMap(map_width, map_height)

        self.createCaves(map_width, map_height) #

        self.getCaves(map_width, map_height)

        self.connectCaves(map_width, map_height)

        dungeon.tiles = self.level
        return dungeon

    def randomFillMap(self, map_width: int, map_height: int):
        for y in range(1,map_height-1):
            for x in range(1,map_width-1):
                if random.random() > self.wallProbability:
                    self.level[x,y] = tile_types.floor

    def createCaves(self, map_width: int, map_height: int):
        for i in range(self.iterations):
            # Pick a random point with a buffer around the edges of the map
            tileX = random.randint(1,map_width-2)
            tileY = random.randint(1, map_height-2)

            # if the cell's neighboring walls > self.neighbors set it to wall
            if self.getAdjacentWalls(tileX, tileY) > self.neighbours:
                self.level[tileX,tileY] = tile_types.wall
            # or set it to floor
            elif self.getAdjacentWalls(tileX, tileY) < self.neighbours:
                self.level[tileX,tileY] = tile_types.floor

    def getAdjacentWalls(self, x: int, y: int) -> int:
        wallcounter = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if self.level[x+i,y+j] == tile_types.wall and (x+i,y+j) != (x,y):
                    wallcounter += 1
        return wallcounter

    def getCaves(self, map_width: int, map_height: int):
        # locate all the caves within self.level and store them in self.caves
        for x in range(0,map_width):
            for y in range(0,map_height):
                if self.level[x,y] == tile_types.floor:
                    self.floodFill(x,y)

        for set in self.caves:
            for tile in set:
                self.level[tile[0],tile[1]] = tile_types.floor

    def floodFill(self, x: int, y: int):
        '''
        flood fill the separate regions of the level, discard
        the regions that are smaller than the minimum room size, and
        create a reference for the rest.
        '''

        cave = set()
        tile = (x,y)
        toBeFilled = set([tile])
        while len(toBeFilled) > 0:
            tile = toBeFilled.pop()

            if tile not in cave:
                cave.add(tile)

                self.level[tile[0],tile[1]] = tile_types.wall

                #check adjacent cells
                x = tile[0]
                y = tile[1]
                north = (x,y-1)
                south = (x,y+1)
                east = (x+1,y)
                west = (x-1,y)

                for direction in [north,south,east,west]:
                    if self.level[direction] == tile_types.floor:
                        if direction not in toBeFilled and direction not in cave:
                            toBeFilled.add(direction)

        if len(cave) > self.ROOM_MIN_SIZE:
            self.caves.append(cave)

    def connectCaves(self, map_width, map_height):
        # Find the closest cave to the current cave
        for currentCave in self.caves:
            for point1 in currentCave: break # get an element from cave1
            point2 = None
            distance = None
            for nextCave in self.caves:
                if nextCave != currentCave and not self.checkConnectivity(currentCave, nextCave):
                    # choose a random point from nextCave
                    for nextPoint in nextCave: break
                    # compare distance of point1 to old and new point2
                    newDistance = self.distanceFormula(point1, nextPoint)
                    if (distance is None) or (newDistance < distance):
                        point2 = nextPoint
                        distance = newDistance
            if point2: # if all tunnels are connected, point2 == None
                self.createTunnel(point1, point2, currentCave, map_width, map_height)

    def distanceFormula(self, point1, point2):
        d = sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
        return d

    def checkConnectivity(self, cave1, cave2):
        # floods cave1, then checks a point in cave2 for the flood

        connectedRegion = set()
        for start in cave1: break

        tobeFilled = set([start])
        while tobeFilled:
            tile = tobeFilled.pop()

            if tile not in connectedRegion:
                connectedRegion.add(tile)

                # check adjacent cells
                x = tile[0]
                y = tile[1]
                north = (x,y-1)
                south = (x,y+1)
                east = (x+1,y)
                west = (x-1,y)

                for direction in [north,south,east,west]:
                    if direction in cave2 and direction not in tobeFilled and direction not in connectedRegion:
                        tobeFilled.add(direction)

        for end in cave2: break

        if end in connectedRegion:
            return True
        else:
            return False

    def createTunnel(self, point1, point2, currentCave, map_width, map_height):
        '''run a heavily weighted random walk to create a tunnel'''

        drunkardX = point2[0]
        drunkardY = point2[1]
        while (drunkardX,drunkardY) not in currentCave:
            # ==== Choose Direction ====
            north = 1.0
            south = 1.0
            east = 1.0
            west = 1.0

            weight = 1

            # weight the random walk against edges
            if drunkardX < point1[0]:
                east += weight
            elif drunkardX > point1[0]:
                west += weight
            if drunkardY < point1[1]:
                south += weight
            elif drunkardY > point1[1]:
                north += weight

            # normalize probabilities so they form a range from 0 to 1
            total = north + south + east + west
            north /= total
            south /= total
            east /= total
            west /= total

            # choose the direction
            choice = random.random()
            if 0 <= choice < north:
                dx = 0
                dy = -1
            elif north <= choice < north + south:
                dx = 0
                dy = 1
            elif north + south <= choice < north + south + east:
                dx = 1
                dy = 0
            else:
                dx = -1
                dy = 0

            # ==== Walk ====
            # check collision at edges
            if (0 < drunkardX + dx < map_width-1) and (0 < drunkardY + dy < map_height-1):
                drunkardX += dx
                drunkardY += dy
                if self.level[drunkardX,drunkardY] == tile_types.wall:
                    self.level[drunkardX,drunkardY] = tile_types.floor