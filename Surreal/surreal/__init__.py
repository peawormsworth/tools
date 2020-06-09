from math import log
from fractions import Fraction

# Surreal python class
# Author: Jeff Anderson
#   Date: 06-07-2020
# all rights reserved
#  no rights transferred

# bits of precision
bits = 16

class Surreal():
    """
    class to represent and manipulate numbers according to surreal algebra.
    The representation is a linked list of binary tuples.
    Standard operators (+,-,*,/) are overloaded.
    """

    def __init__ (x,a=None,b=None):
        """
        Return nan if a and b are missing.
        Return a construction based on the a if it is a number
        Return a construction with the left and right being whatever pair was provided
        """

        if a is b is None:
            x.x = ()
        elif not b and a and type(a) in (int,float,Fraction):
            x.x = x.construct(a).x
        else:
            x.x = a,b

    def __add__ (x,y):
        """return the sum of x and y"""

        a,b = x
        c,d = y
        if x == nil:
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
        """alternate naming for star()"""

        return x.star()

    def star(x):
        """
        return the conjugate/transposition of given number x
        this means nothing for standard surreal numbers (surreals)
        it is hear in case the caller asks for it.
        """

        return x

    def __mul__ (x,y):
        """multiply x times y"""

        a,b = x
        c,d = y
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
        """division is not implemented. Please stand by"""

        return x * ~y

    def __sub__ (x,y):
        """subtract y from x"""

        return x + (-y)

    def __neg__ (x):
        """negate x"""

        if not x:
           return x
        a,b = x
        if not x == nil:
            a,b = -b,-a
        return type(x)(a,b)

    def __pos__ (x):
        "return the positive value of a given number (always itself)"

        return type(x)(x[0],x[1])

    def __invert__ (y):
        """return 1/y, the inversion from input y"""

        if   y == pos : return y
        elif y < nil : return -~-y
        elif y == nil : raise  ZeroDivisionError()
        yl,yr = y
        il = nil
        ir = None
        r  = None,None
        iyr,iyl = None,None
        width = 0
        while (il or ir) and width < 6:
            width += 1
            nl = nr = None
            if il:
                r = (il,r[1])
                if yr:
                    iyr = iyr or ~yr
                    left = (pos+(yr-y)*il)*iyr
                    if not r[0] or left > r[0]:
                       nl = left
                if yl and not (yl <= nil):
                    iyl = iyl or ~yl
                    right = (pos+(yl-y)*il)*iyl
                    if not r[1] or right < r[1]:
                       nr = right
            if ir:
                r = (r[0],ir)
                if yl and not (yl <= nil):
                    iyl = iyl or ~yl
                    left = (pos+(yl-y)*ir)*iyl
                    if not r[0] or (left > r[0] and (not nl or left > nl)):
                        nl = left
                if yr:
                    iyr = iyr or ~yr
                    right = (pos+(yr-y)*ir)*iyr
                    if not r[1] or (right < r[1] and (not nr or right < nr)):
                        nr = right
            il,ir = nl,nr
        return type(y)(*r).reduce()

    def __le__ (x,y):
        """True if x is less than or equal to y"""

        a,b = x
        c,d = y
        return not (a and y <= a or d and d <= x)

    def __gt__ (x,y):
        """True if x is greater than y"""

        return not x <= y

    def __ge__ (x,y):
        """True if x is greater than or equal to y"""

        return y <= x

    def __lt__ (x,y):
        """True if x is less than y"""

        return not y <= x

    def __eq__ (x,y):
        """True if x is equal to y"""

        return x <= y and y <= x

    def __ne__ (x,y):
        """True if x is not equal to y"""

        return not x == y

    def fraction(x):
        """return the numeric value of x as a fraction"""

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

    def __float__(x):
        """return the numeric value of x as a float"""

        return float(x.fraction())

    def __abs__(x):
        """return the absolute value of x as a surreal"""

        return x if nil <= x else -x

    def __len__ (x):
        """return the length of elements in x. Hint: it's 2"""

        return 2

    def __getitem__ (x,n):
        return x.x[n]

    def __repr__ (x):
        return '%s(%s)' % (type(x).__name__, x.x)

    def __str__ (x):
        return '%r' % float(x)

    def form (x):
        """display the value in the standard {R|L} form"""

        return '{{{}|{}}}'.format(str(x[0] or 'Ø'),str(x[1] or 'Ø'))

    def __bool__(x):
        """False when input is Nan, otherwise True"""

        return bool(x.x)

    def num (x):
        """return the numeric value of a surreal"""

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
        """return a surreal construction matching the given number to the defined precision"""

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
        """an equivalent surreal in standard form"""

        if y is None:
            y = nil
        if x <= y:
            if y <= x:
                return y
            return x.reduce(type(x)(y[0],y))
        return x.reduce(type(x)(y,y[1]))

nan = Surreal()
nil = Surreal(nan, nan)
pos = Surreal(nil, nan)
neg = Surreal(nan, nil)

