#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from numpy.random import random_integers as rand

#constants 
MAPA_OCUPADO = 1
MAPA_LIBRE = 0
MAPA_SALIDA = 4
MAPA_INICIO = 5
MAPA_BESTIA = 6


class Maze(object):
    def __init__(self, width=81, height=51, complexity=.75, density=.75):
        
        # Only odd shapes
        shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (shape[0] + shape[1])))
        density    = int(density * (shape[0] // 2 * shape[1] // 2))
        # Build actual maze
        self.Z = numpy.zeros(shape, dtype=numpy.int8)
        # Fill borders
        self.Z[0, :] = self.Z[-1, :] = MAPA_OCUPADO
        self.Z[:, 0] = self.Z[:, -1] = MAPA_OCUPADO
        # Make isles
        for i in range(density):
            x, y = rand(0, shape[1] // 2) * 2, rand(0, shape[0] // 2) * 2
            self.Z[y, x] = MAPA_OCUPADO
            for j in range(complexity):
                neighbours = []
                if x > 1:             neighbours.append((y, x - 2))
                if x < shape[1] - 2:  neighbours.append((y, x + 2))
                if y > 1:             neighbours.append((y - 2, x))
                if y < shape[0] - 2:  neighbours.append((y + 2, x))
                if len(neighbours):
                    y_,x_ = neighbours[rand(0, len(neighbours) - 1)]
                    if self.Z[y_, x_] == MAPA_LIBRE:
                        self.Z[y_, x_] = MAPA_OCUPADO
                        self.Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = MAPA_OCUPADO
                        x, y = x_, y_

        
        # define an exit in empty cell
        while True:
            x, y = rand(0,width//2), rand(0,height//2)
            #print ">" + str(self.Z[x,y])
            if self.Z[x,y] == MAPA_LIBRE:
                self.Z[x,y] = MAPA_SALIDA
                break
        
        # define a start in empty cell
        while True:
            x, y = rand(width//2,width), rand(height//2,height)
            #print ">" + str(self.Z[x,y])
            if self.Z[x,y] == MAPA_LIBRE:
                self.Z[x,y] = MAPA_INICIO
                break
        
        # define enemy cell
        while True:
            x, y = rand(width//2,width), rand(0 ,height//2)
            #print ">" + str(self.Z[x,y])
            if self.Z[x,y] == MAPA_LIBRE:
                self.Z[x,y] = MAPA_BESTIA
                break
            #else:
            #    print self.Z[x,y]
        
        return
     
    def getMap(self):
        return self.Z

        