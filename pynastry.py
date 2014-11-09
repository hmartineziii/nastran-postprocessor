#!/usr/bin/python
# (c)Hector Martinez III

from pyNastran.f06.f06 import F06
from glob import glob


fn= glob('*.f06')
f06 = F06(fn[0])
#f06.setF06Name(f06Name)
f = f06.readF06()

# print f06.gridPointForces