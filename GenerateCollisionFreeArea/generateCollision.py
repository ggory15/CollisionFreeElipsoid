import numpy as np

class generateCollision(object):
    def __init__(self, Config):
        self.n = Config.n
        self.obsx = Config.obsx
        self.obsy = Config.obsy
        self.limit_x = Config.limit_x
        self.limit_y = Config.limit_y

        self.generate()

    def generate(self):
        boundary_x = np.array([[-self.limit_x, -self.limit_x, self.limit_x, self.limit_x],
                                [-self.limit_x, self.limit_x, self.limit_x, -self.limit_x],
                                [-self.limit_x, -self.limit_x, self.limit_x, self.limit_x],
                                [-self.limit_x, self.limit_x, self.limit_x, -self.limit_x]])    
        boundary_y = np.array([[-self.limit_y, self.limit_y, self.limit_y, -self.limit_y],
                                [self.limit_y, self.limit_y, -self.limit_y, -self.limit_y],
                                [-self.limit_y, self.limit_y, self.limit_y, -self.limit_y],
                                [self.limit_y, self.limit_y, self.limit_y, -self.limit_y]])    

        self.xv = np.hstack( (self.obsx.T, boundary_x))
        self.yv = np.hstack( (self.obsy.T, boundary_y))