#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 11:06:40 2019

@author: murray

This is a toy forest fire (/wildfire / brushfire) model. 

0 is unburt tree 
1 is burning
-1 is burnt and now longer fueld

Type 1: randomly generates 3 wildfires and lets them burn to completion
Type 2: as type 1, but with random trees 
Type 3: as type 2, but with different vegitation types 
Type 4: as type 3, but with fire barriers (e.g. river)
Type 5: as type 4, but with embers at the fire front
"""

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import colors

### Global vars 
a = 80 # y model domain
b = 50 # x model domain 
t_p = 0.6 # Proportion of trees to empty space
timesteps = 5
n_starting_fires = 6
veg_types = {"1":1, "2":0.5, "3":0.1, "4":0.55, "5":0.15} # Each key is a different tree type with prob. of ignition.

### Set up model 
forest = np.zeros((a, b, timesteps), dtype=int) - 1 # Initialize an empty forest
def build_forest(forest, veg_types, t_p):
    """
    Builds the forest randomly.
    Reserved values are -1, which is empty, and 0, which is a fire
    """
    # Get number of trees 
    tot_trees = int(forest.size * t_p)
    # Get number of each species
    n_trees = int(np.floor(tot_trees / len(veg_types)))
    # Fill species 
    for i in veg_types:
        forest[np.random.randint(low = 0, high = a, size = n_trees), 
               np.random.randint(low = 0, high = b, size = n_trees), 
               np.zeros(n_trees, dtype=int)] = i
#    temp_a, temp_b = np.indices((a,b))
#    np.random.shuffle(temp_a)
#    np.random.shuffle(temp_b)
#    a = data[:int(N*0.6)]
#    b = data[int(N*0.6):int(N*0.8)]
#    c = data[int(N*0.8):]
#    a = data[:int(N*0.6)]
#    b = data[int(N*0.6):int(N*0.8)]
#    c = data[int(N*0.8):]
    forest[:,0] = -1; forest[:,b-1] = -1; forest[0,:] = -1; forest[a-1,:] = -1
    return forest
forest = build_forest(forest, veg_types, t_p)

### Set up colours 
#colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'orange']
colors_list = [(np.random.beta(0.2,1), 
                np.random.beta(0.8,1,1)[0], 
                np.random.beta(0.2,1)) for i in range(len(veg_types) - 2)]
colors_list.insert(0,"black")
colors_list.insert(1,"orange")
cmap = colors.ListedColormap(colors_list)
bounds = np.arange(-1,int(max((veg_types.keys()))))
norm = colors.BoundaryNorm(bounds, cmap.N)

### Set up neighbourhood
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

### Randomly start fires
forest[(np.random.randint(low=1, high=a-1, size=n_starting_fires), 
        np.random.randint(low=1, high=b-1, size=n_starting_fires), 
        np.zeros((n_starting_fires), dtype=int))] = 0

### Run model 
for t in range(timesteps - 1):
    forest[:,:,t + 1] = forest[:,:,t]
    for a_ind in range(1, a - 1):
        for b_ind in range(1, b - 1):
            if forest[a_ind, b_ind, t] == 0:
                for x, y in neighbourhood:
                    if forest[a_ind + x, b_ind + y, t] > 0:
                        forest[a_ind + x, b_ind + y, t + 1] = 0
                forest[a_ind, b_ind, t + 1] = -1
    plt.imshow(forest[:,:,t], cmap=cmap, norm=norm)
    plt.show()
    plt.close()


### Sandbox 
#forest[:,:,0] 
#
#forest = np.zeros((a, b, timesteps), dtype=int)
#forest[np.random.randint(low = -1, high = 1, size = 5), 
#       np.random.randint(low = -1, high = 1, size = 5), 
#       np.zeros(5, dtype=int)] = -1
#forest[:,0] = -1; forest[:,a-1] = -1; forest[0,:] = -1; forest[b-1,:] = -1
#
#plt.imshow(forest[:,:,0], cmap=cmap, norm=norm)
#plt.show()