import numpy as np
import quadprog_helper as qp


class MinimumPoint(object):
    def __init__(self, C, d, O, i):
        V = O[i].T
        k = V.shape[1] # for w variable
        n = V.shape[0] # for x variable
        V_var = np.dot(np.linalg.pinv(C) , (V - d) )
 
        H = np.matrix(np.identity(k+n))
        for i in range(k):
            H[i, i] = 0.00000001
        
        g = np.array(np.zeros(n+k))
        
        A_test =np.array(np.zeros((1+n, k+n)))
        for i in range(k):
            A_test[0, i] = 1.0
        A_test[1:, : k] = V_var
        A_test[1:, k : ] = (np.identity(n)) * -1.0
 
        b_test =np.array(np.zeros(1+n))
        b_test[0] = 1.0

        G_test = np.array(np.zeros((k, n+k)))
        h_test = np.array(np.zeros(k))
        G_test[:k, :k] = np.array(np.identity(k))*-1.0

        x_var = qp.quadprog_solve_qp(H, g, G_test, h_test, A_test, b_test, None)
        self.x_opt = np.dot(C.T,x_var[k:].reshape(2,1)) + d

    