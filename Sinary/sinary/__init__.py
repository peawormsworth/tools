from fractions import Fraction
import re

class Sinary():
    def __init__(x,v):
        assert(type(v) is int), 'integer expected'
        x.v = v

    def __neg__ (x):
        return type(x)(neg(x))

    def __le__ (x,y):
        return le(x.v,y.v)

    def __gt__ (x,y):
        return gt(x.v,y.v)

    def __ge__ (x,y):
        return ge(x.v,y.v)

    def __lt__ (x,y):
        return lt(x.v,y.v)

    def __eq__ (x,y):
        return eq(x.v,y.v)

    def __ne__ (x,y):
        return ne(x.v,y.v)

    #def __bool__ (x):
        #return bool(x.v)
        #return x.v is not nan

    def __repr__ (x):
        return '%s%r' % (type(x).__name__, (x.left().v, x.right().v))

    def __str__ (x):
        return '%r' % ((x.left().v, x.right().v),)

    def __len__ (x): return 2

    def __getitem__ (x,n):
        if n == 0: return x.left()
        if n == 1: return x.right()
        raise IndexError

    def __int__ (x):
        return x.v

    def pair (x):
        """list of the lessor and greater split of x"""

        return x.left(), x.right()

    def left (x):
        """lessor side of x"""

        return Sinary(side(x.v,1))

    def right (x):
        """greater side of x"""

        return Sinary(side(x.v,0))

    def __add__ (x,y):
        return Sinary(add(x.v,y.v))

    def __sub__ (x,y):
        return Sinary(sub(x.v,y.v))

    def __mul__ (x,y):
        return Sinary(mul(x.v,y.v))

    def __truediv__ (x,y):
        return Sinary(divide(x.v,y.v))

    def __invert__ (x,y):
        return Sinary(invert(x.v,y.v))

    def __neg__ (x,y):
        return Sinary(neg(x,v,y.v))

    def __pos__ (x):
        return Sinary(x.v)

    def __abs__ (x):
        return Sinary(_abs(x.v))

    def __float__ (x):
        return float(label(x))

nan = 0
nil = 1
neg = 2
pos = 3

def _abs (x):
    """return the absolute value of x as a surreal"""

    return x if le(nil,x) else -x

def label (x):
    """return the numeric value of this sinary as a fraction"""

    if x == 0:
        return None
    if x == 1:
        return Fraction(0)
    b = bin(x)[2:]
    s = b[1]
    wf = re.compile(r'^.({}+)(.*)$'.format(s))
    w,f = wf.findall(b)[0]
    p = 1 if s == '1' else -1
    n = p * Fraction(len(w),1)
    scale = Fraction(1,1)
    while len(f):
        scale /= 2
        if f[0] == '1':
            n +=  scale
        else:
            n += -scale
        f = f[1:]
    return n

def num (x):
    """return the numeric value of a curset"""

    if not x:
        return None
    seed  = 1
    scale = Fraction(1,1)
    lone  = None
    num   = Fraction(0,1)
    while not x == seed:

        if not lone and le(_abs(sub(x,seed)),pos):
            lone = True
        if le(seed,x):
            seed = seed*2+1
            num += scale
            lone = lone or le(x,seed)
        else:
            seed = seed*2
            num -= scale
            lone = lone or le(seed,x)
        if lone:
            scale *= Fraction(1,2)
    return num

def side(s,f):

    "returns the lessor side of s"
    if s in (0,1) and f is 1:
        return 0
    while s % 2 != f:
        s //= 2
    return s//2

def split(s):
    "list of the lessor and greater split of s"

    return side(s,1), side(s,0)

def join (xl,xr,y=1):
    """given a left and right sinary, return its equivelent single form"""

    X = (xl,xr)
    Y = split(y)
    while not seq(X,Y):
        y *= 2
        if sle(Y,X): y += 1
        Y = split(y)
    return y

def sle(x,y):
    "less than or equal to comparsion of x and y split representations"

    return not(x[0] and sle(y,split(x[0])) or y[1] and sle(split(y[1]),x))

def seq(x,y):
    "true if x and y are equal"

    return sle(x,y) and sle(y,x)

def le(x,y):
    return sle(split(x),split(y))

def gt (x,y):
    """True if x is greater than y"""

    return not le(x,y)

def ge (x,y):
    """True if x is greater than or equal to y"""

    return le(y,x)

def lt (x,y):
    """True if x is less than y"""

    return not le(y,x)

def ne (x,y):
    """True if x is not equal to y"""

    return not (le(x,y) and le(y,x))

def eq(x,y):
    "true if x and y are equal"

    return le(x,y) and le(y,x)

def add (x,y):
    "add two numbers"

    if x is 1:
        return y
    if y is 1: 
        return x
    xl,xr = split(x)
    yl,yr = split(y)
    left  = xl and add(xl,y)
    right = xr and add(xr,y)
    if yl:
        less = add(x,yl)
        if not left or le(left, less):
            left = less
    if yr:
        more = add(x,yr)
        if not right or le(more, right):
            right = more
    return join(left,right)

def neg(x):
    "flip all bits except the first"

    return x and x^mask(x)

def mask(x,m=0):
    "generate a binary number of all '1's up to one less than the bits of x"

    while x>>1:
        x = x>>1
        m = (m<<1)|1
    #if x>>1:
        #return mask(x>>1,(m<<1)|1)
    return m

def sub (x,y):
    return add(x,neg(y))

def mul (x,y):
    "multiply two numbers"

    if 0 in (x,y): return 0
    if x is 1 or y is 3 : return x
    if y is 1 or x is 3 : return y
    if x is 2 : return -y
    if y is 2 : return -x
    xl,xr = split(x)
    yl,yr = split(y)

    left,right = 0,0
    if xl and yl:
        left  = sub(add(mul(xl,y),mul(x,yl)),mul(xl,yl))
    if xr and yr:
        left2 = sub(add(mul(xr,y),mul(x,yr)),mul(xr,yr))
        if left == 0 or not le(left2,left):
            left = left2
    if xl and yr:
        right  = sub(add(mul(xl,y),mul(x,yr)),mul(xl,yr))
    if xr and yl:
        right2 = sub(add(mul(x,yl),mul(xr,y)),mul(xr,yl))
        if right == 0 or not le(right,right2):
            right = right2
    return reduce(left,right)

def invert (y):
    """return 1/y, the inversion from input y"""

    if   eq(y,pos) : return y
    elif lt(y,nil) : return neg(invert(neg(y)))
    elif eq(y,nil) : raise  ZeroDivisionError()
    yl,yr = split(y)
    il = nil
    ir = None
    r  = None,None
    iyr,iyl = None,None
    width = 0
    while (il or ir) and width < 3:
        width += 1
        nl = nr = None
        if il is not None:
            r = (il,r[1])
            if yr is not None:
                if iyr is None:
                    #iyr = ~yr
                    iyr = invert(yr)
                left = mul(mul(add(pos,sub(yr,y)),il),iyr)
                if r[0] is None or gt(left,r[0]):
                    nl = left
            if yl is not None and not le(yl,nil):
                if iyl is None:
                    #iyl = ~yl
                    iyl = invert(yl)
                right = mul(mul(add(pos,sub(yl,y)),il),iyl)
                if r[1] is None or lt(right,r[1]):
                    nr = right
        if ir:
            r = (r[0],ir)
            if yl is not None and not le(yl,nil):
                if iyl is None:
                    #iyl = ~yl
                    iyl = invert(yl)
                left = mul(mul(add(pos,sub(yl,y)),ir),iyl)
                if r[0] is None or (gt(left,r[0]) and (not nl or gt(left,nl))):
                    nl = left
            if yr is not None:
                if iyr is None:
                    #iyr = ~yr
                    iyr = invert(yr)
                right = mul(mul(add(pos,sub(yr,y)),ir),iyr)
                if r[1] is None or (lt(right,r[1]) and (not nr or lt(right,nr))):
                    nr = right
        il,ir = nl,nr
    #print(r)
    if r[0] is None: r = (0,r[1])
    if r[1] is None: r = (r[0],0)
    return join(*r)

