from Config import obstacle 
from GenerateCollisionFreeArea import generateCollision, OptimalArea
import numpy as np
import os

cols = generateCollision(obstacle)
x0 = np.matrix(np.ones([2,1]))

opt = OptimalArea(x0, cols)
print opt.C, opt.d
