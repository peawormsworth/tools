from math import log
from fractions import Fraction

nan = ()
nil = nan,nan
pos = nil,nan
neg = nan,nil
precision = 2**-8

def delink (x):
    a = [[],[]]
    a[:] = x[:]
    return a
    r = tuple(a)
    return r

class HyperCurset():
    def __init__ (self,*state):
        sl = len(state)
        assert (sl), 'input required'

        log_len = log(sl, 2)
        assert (log_len.is_integer()), 'input list must be a power of 2 (len(list) = 2^n), not %s' % sl

        if sl == 1:
            if type(state[0]) in (list,tuple):
                self.x = state[0]
            else:
                raise TypeError('2 or more arguments are required')

        elif sl == 2:
            if type(state[0]) is HyperCurset:
                self.x = [delink(state[0].x), delink(state[1].x)]
            elif type(state[0]) in (tuple,list):
                self.x = [delink(state[0]), delink(state[1])]
            else:
                self.x = [delink(construct(state[0])), \
                         delink(construct(state[1]))]
        elif sl > 2:
            half = sl // 2
            self.x = [delink(HyperCurset(*state[:half]).x), \
                     delink(HyperCurset(*state[half:]).x) ]

    def __add__ (self,y):
        return HyperCurset(add(self.x,y.x))

    def __mul__ (self,y):
        return HyperCurset(mul(self.x,y.x))

    def __truediv__ (self,y):
        return HyperCurset(divide(self.x,y.x))

    def __sub__ (self,y):
        return HyperCurset(sub(self.x,y.x))

    def __neg__ (self):
        return HyperCurset(negate(self.x))

    def __pos__ (self):
        return HyperCurset(self.x)

    def __invert__ (self):
        # currently set to return 1/x (fractional inverse)
        # should this call conjugate instead? (spacial reflection)
        # should this depend on the type? hyper/curset?
        return HyperCurset(invert(self.x))

    def __le__ (self,y):
        return le(self.x,y)

    def __gt__ (self,y):
        return gt(self.x,y)

    def __ge__ (self,y):
        return ge(self.x,y)

    def __lt__ (self,y):
        return lt(self.x,y)

    def __eq__ (self,y):
        return eq(self.x,y)

    def __ne__ (self,y):
        return ne(self.x,y)

    def __float__(self):
        return float(numeric(self.x))

    def __len__ (self): return 2

    def __getitem__ (self,n):
        return self.x[n]

    def __repr__ (self):
        return '%s(%s)' % (type(self).__name__, self.x)

    def __str__ (self):
        return hyper_str(self.x)

def hyper_str(x):
    if hyper(x):
        return '(' + ', '.join([hyper_str(x[0]), hyper_str(x[1])]) + ')'
    return '%r' % float(numeric(x))

def add (x,y):
    if curset(x):
        return sadd(x,y)
    return [ delink(add(x[0],y[0])) \
           , delink(add(x[1],y[1])) ]

def sub(x,y):
    if curset(x):
        return ssub(x,y)
    return [ delink(sub(x[0],y[0])) \
           , delink(sub(x[1],y[1])) ]

# complex: (a,b) * (c,d) = (ac-d*b,da+bc*)
def mul(x,y):
    if curset(x):
        return smul(x,y)
    return [ delink(sub(mul(x[0],y[0]),mul(conj(y[1]),x[1]))) \
           , delink(add(mul(y[1],x[0]),mul(x[1],conj(y[0])))) ]

def conj(x):
    if curset(x):
        return x
    return [ delink(conj(x[0])), delink(negate(x[1])) ]

def divide (x,y):
    return mul(x,invert(y))

def gt (x,y) : return not le(x,y)
def ne (x,y) : return not le(x,y) and not le(y,x)
def eq (x,y) : return     le(x,y) and     le(y,x)
def ge (x,y) : return                     le(y,x)
def lt (x,y) : return                 not le(y,x)

def le (x,y):
    return not(x[0] and le(y,x[0]) or y[1] and le(y[1],x))

def curset(x):
    return not x or x[0] is x[1] or x[0] in x[1] or x[1] in x[0]

def hyper(x):
    return not curset(x)

def negate (x):
    if hyper(x):
        return [delink(negate(x[0])), delink(negate(x[1]))]
    return (negate(x[1]), negate(x[0])) if x else x

def reduce(x,y=nil):
    if le(x,y):
        if le(y,x):
            return y
        return reduce(x,(y[0],y))
    return reduce(x,(y,y[1]))

def sadd(x,y):
    if not x or not y: return x or y
    a,b = x
    c,d = y
    l = sadd(a,y) if a else a
    r = sadd(b,y) if b else b
    if c:
        less = sadd(x,c)
        if not l or le(l, less):
            l = less
    if d:
        more = sadd(x,d)
        if not r or le(more, r):
            r = more
    return reduce((l,r))

def ssub (x,y):
    return sadd(x,negate(y))

def smul (x,y):
    if not x or eq(y,pos): return x
    if not y or eq(x,pos): return y
    if eq(x,neg): return negate(y)
    if eq(y,neg): return negate(x)
    xl,xr = x
    yl,yr = y
    left,right = nil
    if xl and yl:
        left  = sub(add(smul(xl,y),smul(x,yl)),smul(xl,yl))
    if xr and yr:
        left2 = sub(add(smul(xr,y),smul(x,yr)),smul(xr,yr))
        if not left or le(left,left2):
            left = left2
    if xl and yr:
        right  = sub(add(smul(xl,y),smul(x,yr)),smul(xl,yr))
    if xr and yl:
        right2 = sub(add(smul(x,yl),smul(xr,y)),smul(xr,yl))
        if not right or le(right2,right):
            right = right2
    return reduce((left,right))

def invert (y):
    if   eq(y,pos): return y
    elif lt(y,nil): return negate(invert(negate(y)))
    elif eq(y,nil): raise  ZeroDivisionError()
    yl,yr = y
    il = nil
    ir = None
    r  = None,None
    iyr,iyl = None,None
    while il or ir:
        nl = nr = None
        if il:
            r = (il,r[1])
            if yr:
                iyr = iyr or invert(yr)
                left = smul(add(pos,smul(sub(yr,y),il)),iyr)
                if not r[0] or gt(left,r[0]):
                   nl = left
            if yl and not le(yl,nil):
                iyl = iyl or invert(yl)
                right = smul(add(pos,smul(sub(yl,y),il)),iyl)
                if not r[1] or lt(right,r[1]):
                   nr = right
        if ir:
            r = (r[0],ir)
            if yl and not le(yl,nil):
                iyl = iyl or invert(yl)
                left = smul(add(pos,smul(sub(yl,y),ir)),iyl)
                if not (nl and le(left,nl) or r[0] and le(left,r[0])):
                    nl = left
            if yr:
                iyr = iyr or invert(yr)
                right = smul(add(pos,smul(sub(yr,y),ir)),iyr)
                if not (nr and le(right,nr) or r[1] and le(right,r[1])):
                    nr = right
        il,ir = nl,nr
    return reduce(r)

# Tools:

def construct (num,precision=precision):
    if num is None: return nan
    seed  = nil
    scale = 1
    lone  = None
    while precision <= abs(num):
        if abs(num) <= 1:
            lone = True
        if num <= 0:
            seed = (seed[0],seed)
            num += scale
            lone = 0 <= num or lone
        else:
            seed = (seed,seed[1])
            num -= scale
            lone = num <= 0 or lone
        if lone:
            scale /= 2
    return seed

# return the numeric value of a curset
def numeric (x):
    seed  = nil
    scale = 1
    lone  = None
    num   = Fraction(0/1)
    while not eq(x,seed):
        if not lone and within(x,seed,pos):
            lone = True
        if le(seed,x):
            seed = seed,seed[1]
            num += scale
            lone = lone or le(x,seed)
        else:
            seed = seed[0],seed
            num -= scale
            lone = lone or le(seed,x)
        if lone:
            scale /= 2
    return num

# return the sinary (surreal binary) value of a curset
def sinary (x=None):
    seed  = nil
    scale = 1
    lone  = None
    num   = ''
    if x:
        num = '1'
        while not eq(x,seed):
            if not lone and within(x,seed,pos):
                lone = True
            if le(seed,x):
                seed = seed,seed[1]
                num += '1'
                lone = lone or le(x,seed)
            else:
                seed = seed[0],seed
                num += '0'
                lone = lone or le(seed,x)
            if lone:
                scale /= 2
    return num

def within(a,b,c):
    return lt(absolute(sub(a,b)),c)

def absolute(x):
    return x if le(nil,x) else negate(x)

