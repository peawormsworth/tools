from fractions import Fraction
from curset import *

# display the location of nans within the list array
def nodes(x,idx=[]):
    if x == nan:
        print('x[{}] = Ø'.format("][".join(str(i) for i in idx[:])))
    else:
        nodes(x[0],idx+[0])
        nodes(x[1],idx+[1])

# nan bracketed string representation
def nan_str (x):
    # there is a better way...
    return repr(x).replace(type(x).__name__,'').replace('((...))','Ø').replace('((Ø, Ø))','Ø').replace('((','(').replace('))',')')

def canal (r=[Fraction(0,1)]):
    """yeilds fractions according to their birthday ordering.
    0,-1,1,-2,-1/2,1/2,2,-3... 
    """
    yield None
    yield r[0]
    while 1:
        yield r[0] - 1
        rn = [r[0]]
        for n in r[1:]:
            m = (rn[-1]+n)/2
            yield m
            rn.extend((m,n))
        yield rn[-1]+1
        r = [rn[0]-1] + rn + [rn[-1]+1]

def cleave ():
    """yeilds linked lists according to their birthday ordering
    set l to be your nil.
    """
    yield nan
    yield nil
    l = [nil]
    while 1:
        nl  = []
        for s in l:
            h = Curset(s[0],s)
            yield h
            nl = nl + [h]

            h = Curset(s,s[1])
            yield h
            nl = nl + [h]

        l = nl

def create (days=7):
    birth    = canal()
    sprout   = cleave()
    universe = {}
    for i in range(2**days):
        universe[next(birth)] = next(sprout)
    return universe

