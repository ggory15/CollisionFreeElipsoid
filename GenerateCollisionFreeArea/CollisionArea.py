import numpy as np
from MinimumDistance import MinimumDist
from MinimumPoint import MinimumPoint
from tangentP import tangentP
import cvxpy as cp
import copy

class OptimalArea(object):
    def __init__(self, x0, cols):
        self.xv = cols.xv
        self.yv = cols.yv

        self.x = np.array(self.xv[0:3, :])
        self.y = np.array(self.yv[0:3, :])
        
        self.O = []
        for i in range(len(self.x.T)):
            self.O.append( np.hstack( ( np.reshape(self.x[:,i], (3,1)), np.reshape(self.y[:,i], (3,1))) )) 
        
        self.C = 0.01 * (np.array([[1, 0 ], [0, 1]]))
        self.d = x0

        self.iter = 0
        self.area = np.linalg.det(self.C)
        self.threshold = 0.01
        self.growth = 100

        while self.growth > self.threshold:
            self.compute()    

    def compute(self):
        O_remaining = copy.deepcopy(self.O)
   
        num_vertices = O_remaining[0].shape[0]
        dim = O_remaining[0].shape[1]
        self.iter += 1

        A = []
        b = []    
        A1 = []    


        while len(O_remaining)is not 0:
            CloestObstacle = MinimumDist(self.C, self.d, O_remaining)
            l_star = CloestObstacle.d
            CloestDist = MinimumPoint(self.C, self.d, O_remaining, l_star)
            x_star = CloestDist.x_opt
            Tangent = tangentP(self.C, self.d, x_star)

            if len(A) is 0:
                A = Tangent.a.T
                b = Tangent.b
            else:
                A = np.vstack((A, Tangent.a.T))
                b= np.vstack((b, Tangent.b))

                
            O_excluded = l_star
            for j in range(len(O_remaining)):
                if ( np.dot (Tangent.a.T, O_remaining[j].T) >= Tangent.b).all():
                    O_excluded = np.hstack((O_excluded, j))

            O_remaining = np.delete(O_remaining, O_excluded, 0)
            


        prev_C = self.C
        prev_d = self.d
        sizeA = A.shape
        n = sizeA[1]
        m = sizeA[0]

        C = cp.Variable( (n, n), symmetric=True)
        d = cp.Variable( (n,))
        

        # There is some bug about A, b
        A2=np.random.randn(5,2)
        for i in range(5):
            for j in range(2):
                A2[i, j] = A[i, j]
    
        b2=np.random.randn(5)
        for i in range(5):
            b2[i] = b[i]
      
        constr = []
        constr = [cp.norm(  C * A2[i,:].T) + A2[i, :] * d <= b2[i] for i in range(m) ]
        prob =cp.Problem(cp.Maximize(cp.log_det(C)), constr)
        prob.solve(verbose=False)
       
        self.C = np.array(C.value).flatten().reshape(2,2)
        self.d = np.reshape(np.array(d.value).flatten(), (2,1))

        self.growth = (np.linalg.det(self.C) - np.linalg.det(prev_C))/ np.linalg.det(prev_C)
    

        
