import numpy as np

class Triangle:
    def __init__(self, tri):
        self.a = tri[0]
        self.b = tri[1]
        self.c = tri[2]

    def closestPointToPoint(self, p):
        a = self.a
        b = self.b
        c = self.c

        # algorithm thanks to Real-Time Collision Detection by Christer Ericson,
		# published by Morgan Kaufmann Publishers, (c) 2005 Elsevier Inc.,
		# under the accompanying license; see chapter 5.1.5 for detailed explanation.
		# basically, we're distinguishing which of the voronoi regions of the triangle
		# the point lies in with the minimum amount of redundant computation.

        _vab = b - a
        _vac = c - a
        _vap = p - a
        d1 = np.dot(_vab, _vap)
        d2 = np.dot(_vac, _vap)
        if (d1 <=0 and d2 <= 0):
            # vertex region of A; barycentric coords (1, 0, 0)
            return a
        
        _vbp = p - b
        d3 = np.dot(_vab, _vbp)
        d4 = np.dot(_vac, _vbp)
        if (d3 >= 0 and d4 <= d3):
            # vertex region of B; barycentric coords (0, 1, 0)
            return b
        
        vc = d1 * d4 - d3 * d2
        if (vc <= 0 and d1 >= 0 and d3 <= 0 ):
            v = d1 / ( d1 - d3 )
			# edge region of AB; barycentric coords (1-v, v, 0)
            return a + _vab * v
        
        _vcp = p - c
        d5 = np.dot(_vab, _vcp)
        d6 = np.dot(_vac, _vcp)
        if (d6 >= 0 and d5 <= d6):
			# vertex region of C; barycentric coords (0, 0, 1)
            return c
        
        vb = d5 * d2 - d1 * d6
        if ( vb <= 0 and d2 >= 0 and d6 <= 0 ):
            w = d2 / ( d2 - d6 )
            # edge region of AC; barycentric coords (1-w, 0, w)
            return a + _vac * w
        
        va = d3 * d6 - d5 * d4
        if ( va <= 0 and (d4 - d3) >= 0 and (d5 - d6) >= 0):
            _vbc = c - b
            w = (d4 - d3) / ((d4 - d3) + (d5 - d6))
            # edge region of BC; barycentric coords (0, 1-w, w)
            return b + _vbc * w # edge region of BC
        
        # face region
        denom = 1 / (va + vb + vc)
        # u = va * denom
        v = vb * denom
        w = vc * denom
        
        return a + _vab * v + _vac * w
