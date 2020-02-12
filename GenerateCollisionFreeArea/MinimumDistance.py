import numpy as np
import copy
class MinimumDist(object):
    def __init__(self, C, d, O):
        self.O = copy.deepcopy(O)
        self.Cinv = np.linalg.pinv(C)
        self.number_obs = len(O)

        self.min_distance = np.array(np.zeros((1, self.number_obs)))
        
        for idx in range(self.number_obs):
            self.O[idx][:, 0] = self.O[idx][:, 0] - d[0, 0]
            self.O[idx][:, 1] = self.O[idx][:, 1] - d[1, 0]

            self.O[idx] =  np.dot(self.Cinv ,self.O[idx].T).T
            self.min_distance[0, idx] = min(np.linalg.norm(self.O[idx].T, axis=0)) 
        
        
        self.d = np.argmin(self.min_distance)
        self.min_dist = self.min_distance[0, 0]
        
