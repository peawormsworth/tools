# -*- coding: utf-8 -*-
# $Id: involution/__init__.py $
# Author: Jeff Anderson <truejeffanderson@gmail.com>
# Copyright: AGPL
"""

involution

python class for Cayley Dickson construction and operation

source: https://github.com/peawormsworth
author: Jeffrey B Anderson - truejeffanderson at gmail.com
"""

import re
import numpy as np
from math import sqrt, log, ceil

class Algebra():
    """
    Generate involution algebras of Cayley Dickson constructions.

    provides a multi-dimensional number calculator for vaious dimensions and algebraic forms and relationships.
    
    see: involution.albegra for common algebraic constructions.
    """

    precision = 10 ** -9
    str_func  = None

    # convert between input and internal format: '-0+' <=> '012'
    ii_to_internal = str.maketrans('-0+','012')
    ii_to_external = str.maketrans('012','-0+')
    match_ii = re.compile(r'^[-+0]+$')
    match_dp = re.compile(r'^[0-7]+$')

    def conj (m):
        """conjugate this object"""
        #conj = m._conj(m[:])
        conj = -m[:]
        conj[0] *= -1
        return m.__class__(conj, dp=m.dp, ii=m.ii.translate(m.ii_to_external))
        
    # look into np.conjugate() and remove this routine...
    def _conj(m,x):
        """conjugate a given list according to the construct of this object"""
        if x is None:
            conj = -m[:]
        else:
            conj = -x
        conj[0] *= -1
        return conj


    def _curse_mul (m,x,y):
        """recursively multiply the list according to the construction of this object"""
        n = len(x)
        h = n // 2
        #print('here')
        #print('n:',n)
        #print('h:',h)
        if h:
            a,b = x[:h],x[h:]
            c,d = y[:h],y[h:]
            new_state = [None] * n
            #m.state = np.asarray(state)
            #print('state:',m.state)
            #print('new_state:',new_state)
            z = np.asarray(new_state)
            #print('z:',z)
            
            #z = np.zeros(n)
            level = int(log(h,2))
            #print('ii:',m.ii[level])
            ii = int(m.ii[level]) - 1
            def pos(x): return   x
            def neg(x): return  -x
            def zer(x): return x-x
            if ii ==  1: op = pos
            if ii ==  0: op = zer
            if ii == -1: op = neg
            
            #print('ii[%s]: %s' % (level,ii))
            dp = m.dp[level]
            mult = m._curse_mul
            if dp == '0':
                #z[:h] = mult(c,a) + ii * mult(m._conj(b),d)
                z[:h] = mult(c,a) + op(mult(m._conj(b),d))
                z[h:] = mult(d,m._conj(a)) + mult(b,c)
            if dp == '1':
                #z[:h] = mult(c,a) + ii * mult(d,m._conj(b))
                z[:h] = mult(c,a) + op(ii * mult(d,m._conj(b)))
                z[h:] = mult(m._conj(a),d) + mult(c,b)
            if dp == '2':
                #z[:h] = mult(a,c) + ii * mult(m._conj(b),d)
                z[:h] = mult(a,c) + op(mult(m._conj(b),d))
                z[h:] = mult(d,m._conj(a)) + mult(b,c)
            if dp == '3':
                #z[:h] = mult(a,c) + ii * mult(d,m._conj(b))
                #print('a:',a)
                #print('b:',b)
                #print('c:',c)
                #print('d:',d)
                #print(mult(d,m._conj(b)))
                z[:h] = mult(a,c) + op(mult(d,m._conj(b)))
                z[h:] = mult(m._conj(a),d) + mult(c,b)
            if dp == '4':
                #z[:h] = mult(c,a) + ii * mult(b,m._conj(d))
                z[:h] = mult(c,a) + op(mult(b,m._conj(d)))
                z[h:] = mult(a,d) + mult(m._conj(c),b)
            if dp == '5':
                #z[:h] = mult(c,a) + ii * mult(m._conj(d),b)
                z[:h] = mult(c,a) + op(mult(m._conj(d),b))
                z[h:] = mult(d,a) + mult(b,m._conj(c))
            if dp == '6':
                #z[:h] = mult(a,c) + ii * mult(b,m._conj(d))
                z[:h] = mult(a,c) + op(mult(b,m._conj(d)))
                z[h:] = mult(a,d) + mult(m._conj(c),b)
            if dp == '7':
                #z[:h] = mult(a,c) + ii * mult(m._conj(d),b)
                z[:h] = mult(a,c) + op(mult(m._conj(d),b))
                z[h:] = mult(d,a) + mult(b,m._conj(c))

        else:
            z = x * y
        return z


    def __mul__ (m,o):
        """multiply two objects of similar type"""
        try: 
            o_state = o.state
        except:
            o_state = np.zeros(len(m))
            o_state[0] = o
        return m.__class__(m._curse_mul(m.state,o_state), dp=m.dp, ii=m.ii.translate(m.ii_to_external))


    def __abs__ (m,state=None):
        """absolute value of this object"""
        if state is None:
            return m.__abs__(m.state)
        h = len(state) // 2
        if h:
            a,b = state[:h],state[h:]
            # obtain imaginary squared value based on list size...
            level = ceil(log(h,2))
            ii = int(m.ii[level]) - 1
            def pos(x): return   x
            def neg(x): return  -x
            def zer(x): return x-x
            if ii ==  1: op = pos
            if ii ==  0: op = zer
            if ii == -1: op = neg
            #return sqrt(m.__abs__(a) ** 2 - ii * m.__abs__(b) ** 2)
            #return sqrt(m.__abs__(a) * m.__abs__(a) - op(m.__abs__(b) * m.__abs__(b)))
            return sqrt(m.__abs__(a*a) - op(m.__abs__(b * b)))
        return state[0]


    def __getitem__ (m, index=None):
        """the coefficient of the basis for the provided index"""
        return m.state[index]


    def __add__ (m, z):
        """Addition: z1+z2 = (a,b)+(c,d) = (a+c,b+d) auto called for: a+b"""
        try:
            sum = m.state + z.state
        except:
            sum = m[:].tolist()
            sum[0] = sum[0] + z
        return m.__class__(sum, dp=m.dp, ii=m.ii.translate(m.ii_to_external))

        return int(log(len(m),2))


    def level (m):
        """object level is 1 for list size of two and incrments as list size doubles"""
        return int(log(len(m),2))


    def __len__ (m):
        """object length as a count of dimensions or list size"""
        return len(m.state)


    def __str__ (m):
        """generic string function caller"""
        return m.str_func()

    def str_ijk (m):
        """output the object in a readable form (i,j,k notation)"""
        string = ''
        if len(m) > 16:
            symbols = 'abcdefghijklmnopqrstuvwxyzABCDEF'
        else:
            symbols = ' ijklmnopqrstuvwx'
        for i in range(len(m)):
            try:
                value = abs(m[i])
                if value:
                    sign = ''
                    if m[i] > 0:
                        if len(string):
                            sign = sign + '+'
                    else:
                        sign = sign + '-'
                        pass
                    if value % 1 < m.precision:
                        value = int(value)
                    if value == 1 and i:
                        value = ''
                    if i:
                        symbol = symbols[i]
                    else:
                        symbol = ''
                    string += sign + str(value) + symbol
            except:
                if string:
                    string = string + ',' + str(m[i])
                else:
                    string = str(m[i])
        if string == '':
            string = '0'
        elif re.search(r'[+-]',string) is not None:
            #string = '(' + string + ')'
            pass
        return string


    def __repr__ (m):
        """replicate: output this number as a string suitable for evaluation"""
        return "%r([%s], dp=%r, ii=%r)" % (str(type(m).__name__), 
            ','.join(map(str,m[:])), m.dp, m.ii.translate(m.ii_to_external))


    def __radd__ (m, z):
        """Called for a+b, when a is a number and b is this class"""
        return m + z


    def __rsub__ (m, z):
        """Called for a-b, where a is a number and b is of this class"""
        return -m + z


    def __sub__ (m, z):
        """Subtraction: z1-z2 = (a,b)-(c,d) = (a-c,b-d) auto called for a-b"""
        return m + -z


    def __rmul__ (m, z):
        """Called for a*b, where a is a number and b is of this class"""
        return m * z


    def __rtruediv__ (m, z):
        """Called for a/b, where a is a number and b is of this class"""
        return ~m * z


    def __truediv__ (m, z):
        """Division: z1/z2 = (a,b) × (c,d)⁻¹ = (a,b) × inverse(c,d)"""
        if isinstance(z, Algebra):
            return  ~z * m
        else:
            return 1/z * m


    def __invert__ (m):
        """Invert: z⁻¹. called with ~ object"""
        return m.conj()  * (1/abs(m) ** 2)


    def __neg__ (m):
        """Negate: -z = -1 × z. called automatically with -obj"""
        return -1 * m


    def __pos__ (m):
        """Positive: +z = z"""
        return 1 * m


    def replace (m, z):
        """Replace: the existing coefficients with those of the given one"""
        print('new state: ', z)
        m.state = z.state.copy()
        return m


    def __iadd__ (m, z):
        """Addition with assignment: z += x"""
        return m.replace(m + z)


    def __isub__ (m, z):
        """Subtraction with assignment: z -= x"""
        return m.replace(m / z)


    def __imul__ (m, z):
        """Multiplication with assignment: z *= x"""
        return m.replace(m * z)


    def __idiv__ (m, z):
        """Division with assignment: z /= x"""
        return m.replace(m / z)


    def __eq__ (m, z):
        """Equality condition: true if z = x"""
        return abs(m - z) <= m.precision


    def __ne__ (m, z):
        """Inequality: true is z ≠ x"""
        return not m == z

    def dim(m):
        return 2 ** len(m.dp)

    def normalize (m):
        """Normalize: z/|z| = zn, where norm of zn = 1"""
        return m / abs(m)


    # ii has the form '+- +' where:
    #   '+' means i^2 = +1
    #   '-' means i^2 = -1
    #   '0' means i^2 =  0
    #   and the most right character represents the 2d imaginary square
    #
    # dp has the form '32730' where each digits is 0..7 and the number
    #   represents the doubling product selection described in __curse_mul__()
    #
    def __init__ (m, state, dp=None, ii=None, str_func=None):
        """object constructor"""
        try:
            import involution.algebra
            # check list input is an even 2^n
            state_len = len(state)
            assert(state_len), 'input list required'
            log_len   = log(state_len, 2)
            assert(log_len.is_integer()), 'input list must be a power of 2 (len(list) = 2^n), not %s' % len(state)
            if dp:
                assert(2 ** len(dp) == len(state)), 'dp string length must be %s chars (2^n), not %s chars (%s)' % (log_len, len(dp), dp)
                assert(m.match_dp.match(dp)), "dp string may only contain numbers 0 to 7, not '%s'" % dp
            if ii:
                assert(2 ** len(ii) == len(state)), 'ii length must be %s chars (2^n), not %d chars (%s)' % (log_len, len(ii), ii)
                assert(m.match_ii.match(ii)), "ii may only contains negative, positive and empty space: '-+0', not '%s'" % ii
                # internally ii uses characters '012' to hold the sign and just subtracts one when it needs to do math with it.

            #m.state = np.asarray(state, dtype=np.float64)
            m.state = np.asarray(state)

            if dp:
                m.dp = dp
            elif m.dp is None:
                m.dp = '3' * m.level()

            if ii:
                m.ii = ii
            elif m.ii is None:
                m.ii = '0' * m.level()
            m.ii = m.ii.translate(m.ii_to_internal)

            if str_func:
                m.str_func = str_func
            elif m.str_func is None:
                m.str_func = m.str_ijk

        except:
            print("unknown exception here")
            raise
        

