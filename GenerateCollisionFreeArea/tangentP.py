import numpy as np
from numpy import hstack, vstack

class tangentP(object):
    def __init__(self, C, d, x):
        self.a =  2 * np.dot( np.linalg.pinv(C), np.dot(np.linalg.pinv(C.T) , (x -d))) 
        self.b = np.dot(self.a.T , x)
