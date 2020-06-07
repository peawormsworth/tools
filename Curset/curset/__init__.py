from math import log
from fractions import Fraction

# bits of precision
bits = 16

class Curset():
    def __init__ (x,a=None,b=None):
        if a is b is None:
            x.x = x,x
        elif not b and a and type(a) in (int,float,Fraction):
            x.x = x.construct(a).x
        else:
            x.x = a,b

    def __add__ (x,y):
        a,b = x
        c,d = y
        if type(x) is Hyper:
            l,r = a+c,b+d
            return type(x)(l,r)
        elif x == nil:
            l,r = y
        elif y == nil:
            l,r = x
        else:
            a,b = x
            c,d = y
            l = a+y if a else a
            r = b+y if b else b
            if c:
                less = x+c
                if not l or l <= less:
                    l = less
            if d:
                more = x+d
                if not r or more <= r:
                    r = more
        result = type(x)(l,r)
        return result.reduce()

    def conjugate(x):
        return x.star()

    def star(x):
        if type(x) is Hyper:
            a,b = x
            return type(x)(a.star(),-b)
        return x

    def __mul__ (x,y):
        a,b = x
        c,d = y
        if type(x) is Hyper:
            result = a*c - d.star()*b, d*a + b*c.star()
            return type(x)(*result)
        if not x or y == pos : return x
        if not y or x == pos : return y
        if x == neg : return -y
        if y == neg : return -x
        xl,xr = x
        yl,yr = y
        left,right = nil
        if xl and yl:
            left  = xl*y + x*yl - xl*yl
        if xr and yr:
            left2 = xr*y + x*yr - xr*yr
            if not left or left <= left2:
                left = left2
        if xl and yr:
            right  = xl*y + x*yr - xl*yr
        if xr and yl:
            right2 = x*yl + xr*y - xr*yl
            if not right or right2 <= right:
                right = right2
        result = type(x)(left,right)
        return result.reduce()

    def __truediv__ (x,y):
        raise NotImplementedError('division is incomplete') 

    def __sub__ (x,y):
        return x + (-y)

    def __neg__ (x):
        if x == nan:
           return x
        a,b = x
        if type(x) is Hyper:
            a,b = -a,-b
        elif not x == nil:
            a,b = -b,-a
        return type(x)(a,b)

    def __pos__ (x):
        return type(x)(x[0],x[1])
    
    def __invert__ (x):
        return type(x)(invert(x.x))

    def __le__ (x,y):
        a,b = x
        c,d = y
        return not (a and y <= a or d and d <= x)

    def __gt__ (x,y):
        return not x <= y

    def __ge__ (x,y):
        return y <= x

    def __lt__ (x,y):
        return not y <= x

    def __eq__ (x,y):
        if type(x) is Hyper:
           a,b = x
           c,d = y
           return a == c and b == d
        return x <= y and y <= x

    def __ne__ (x,y):
        return not x == y

    def fraction(x):
        return x.num()

    def __float__(x):
        return float(x.num())

    def __abs__(x):
        return x if nil <= x else -x

    def __len__ (x): return 2

    def __getitem__ (x,n):
        return x.x[n]

    def __repr__ (x):
        return '%s(%s)' % (type(x).__name__, x.x)

    def __str__ (x):
        if type(x) is Hyper:
            return '(' + ', '.join([str(x[0]), str(x[1])]) + ')'
        return '%r' % float(x)

    def __bool__(x):
        a,b = x
        return not(x is a is b)

    # return the numeric value of a curset
    def num (x):
        seed = nil
        scale = 1
        lone  = None
        num   = Fraction(0/1)
        while not x == seed:
            if not lone and abs(x-seed) <= pos:
                lone = True
            if seed <= x:
                seed = type(x)(seed, seed[1])
                num += scale
                lone = lone or x <= seed
            else:
                seed = type(x)(seed[0], seed)
                num -= scale
                lone = lone or seed <= x
            if lone:
                scale /= 2
        return num

    def construct (x,num,bits=bits):
        if num is None: return nan
        seed  = nil
        scale = 1
        lone  = None
        while 2**-bits <= abs(num):
            if abs(num) <= 1:
                lone = True
            if num <= 0:
                seed = type(x)(seed[0],seed)
                num += scale
                lone = 0 <= num or lone
            else:
                seed = type(x)(seed,seed[1])
                num -= scale
                lone = num <= 0 or lone
            if lone:
                scale /= 2
        return seed

    def reduce(x,y=None):
        if y is None:
            y = nil
        if x <= y:
            if y <= x:
                return y
            return x.reduce(type(x)(y[0],y))
        return x.reduce(type(x)(y,y[1]))

class Hyper(Curset):
    def __init__ (x,*s):
        l = len(s)
        assert(log(l,2).is_integer()), \
            'input list must be a power of 2, not %s' % l
        if l > 2:
            h = l//2
            x.x = type(x)(*s[:h]), type(x)(*s[h:])
        elif l == 2:
            if type(s[0]) in (int,float,Fraction):
                 x.x = Curset(s[0]), Curset(s[1])
            else:
                 x.x = s[0], s[1]

nan = Curset()
nil = Curset(nan, nan)
pos = Curset(nil, nan)
neg = Curset(nan, nil)
