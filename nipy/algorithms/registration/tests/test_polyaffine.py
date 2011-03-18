import numpy as np 

from nipy.algorithms.registration.polyaffine import *
from nipy.algorithms.registration.c_bindings import _apply_polyaffine
from nipy.algorithms.registration.affine import *

def random_affine():
    T = np.eye(4) 
    T[0:3,0:4] = np.random.rand(3, 4)
    return T 

def id_affine():
    return np.eye(4) 


NCENTERS = 5
NPTS = 100

centers = [np.random.rand(3) for i in range(NCENTERS)]
raf = random_affine()
affines = [raf for i in range(NCENTERS)]
#affines = [id_affine() for i in range(NCENTERS)]
sigma = 1.0
xyz = np.random.rand(NPTS, 3) 

# test 1: crach test create polyaffine transform
T = PolyAffine(centers, affines, sigma) 

# test 2: crash test apply method
t = T.apply(xyz) 

# test 3: check apply does nice job
c = np.array(centers)
tc = T.apply(c) 
qc = np.array([np.dot(a[0:3,0:3], b) + a[0:3,3] for a, b in zip(affines, centers)])

# test 4: crash test compose method
A = Affine(random_affine())
TA = T.compose(A)

# test 5: crash test left compose method
AT = A.compose(T) 

z = AT.apply(xyz) 
za = A.compose(Affine(raf)).apply(xyz)


"""
qc = c.copy()

_affines = np.reshape(np.array(affines)[:,0:3,:], (NCENTERS, 12))
_sigma = np.zeros(3)
_sigma[:] = np.maximum(sigma, 1e-200)
_apply_polyaffine(qc, c, _affines, _sigma) 
"""


