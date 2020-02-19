#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
involution.albegra Unit Tests

general class wide, product table, algebraic, identity and quantum emulation tests

  file: test.py
source: https://github.com/peawormsworth/PyInvolution
author: Jeffrey B Anderson - truejeffanderson at gmail.com
"""

from involution.algebra import *
from surreal import creation
import unittest
import pandas as pd
from math import sqrt
from random import random, uniform

VERBOSE = 1
DEBUG   = 1

s = creation(days=7)
zer = s[0]
one = s[1]
neg = s[-1]

# Class function to run any test here by class object...
from io import StringIO
def run_test(test_class):
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(unittest.makeSuite(test_class))

# Test Data...

complex_table = """
    1  i
    i -1
"""
#{{|}|},{|} {|},{{|}|} 
#{|},{{|}|} {|{|}},{|}

dual_table = """
    1  i
    i  0
"""

split_table = """
    1  i
    i  1
"""

quaternion_table = """
    1  i  j  k
    i -1  k -j
    j -k -1  i
    k  j -i -1
"""

split_quaternion_table = """
    1  i  j  k
    i -1  k -j
    j -k  1 -i
    k  j  i  1 
"""

dual_complex_table = """
    1  i  j  k
    i -1  k -j
    j -k  0  0
    k  j  0  0
"""

hyperbolic_quaternion_table = """
    1  i  j  k
    i  1  k  j
    j -k  1 -i
    k -j  i -1
"""

# not currently used...
bicomplex_table = """
    1  i  j  k
    i -1  k -j
    j  k  1  i
    k -j  i -1
"""

# not currently used...
split_quaternion_table = """
    1  i  j  k
    i -1  k -j
    j -k  1 -i
    k  j  i  1
"""

octonion_table = """
    1  i  j  k  l  m  n  o  
    i -1  k -j  m -l -o  n 
    j -k -1  i  n  o -l -m 
    k  j -i -1  o -n  m -l 
    l -m -n -o -1  i  j  k 
    m  l -o  n -i -1 -k  j
    n  o  l -m -j  k -1 -i 
    o -n  m  l -k -j  i -1
"""

split_octonion_table = """
    1  i  j  k  l  m  n  o  
    i -1  k -j -m  l -o  n 
    j -k -1  i -n  o  l -m 
    k  j -i -1 -o -n  m  l 
    l  m  n  o  1  i  j  k 
    m -l -o  n -i  1  k -j 
    n  o -l -m -j -k  1  i 
    o -n  m -l -k  j -i  1
"""

dual_quaternion_table = """
    1  i  j  k  l  m  n  o
    i -1  k -j  m -l  o -n
    j -k -1  i  n -o -l  m
    k  j -i -1  o  n -m -l
    l -m -n -o  0  0  0  0
    m  l  o -n  0  0  0  0
    n -o  l  m  0  0  0  0
    o  n -m  l  0  0  0  0
"""

sedenion_table = """
    1  i  j  k  l  m  n  o  p  q  r  s  t  u  v  w
    i -1  k -j  m -l -o  n  q -p -s  r -u  t  w -v
    j -k -1  i  n  o -l -m  r  s -p -q -v -w  t  u
    k  j -i -1  o -n  m -l  s -r  q -p -w  v -u  t
    l -m -n -o -1  i  j  k  t  u  v  w -p -q -r -s
    m  l -o  n -i -1 -k  j  u -t  w -v  q -p  s -r
    n  o  l -m -j  k -1 -i  v -w -t  u  r -s -p  q
    o -n  m  l -k -j  i -1  w  v -u -t  s  r -q -p
    p -q -r -s -t -u -v -w -1  i  j  k  l  m  n  o
    q  p -s  r -u  t  w -v -i -1 -k  j -m  l  o -n
    r  s  p -q -v -w  t  u -j  k -1 -i -n -o  l  m
    s -r  q  p -w  v -u  t -k -j  i -1 -o  n -m  l
    t  u  v  w  p -q -r -s -l  m  n  o -1 -i -j -k
    u -t  w -v  q  p  s -r -m -l  o -n  i -1  k -j
    v -w -t  u  r -s  p  q -n -o -l  m  j -k -1  i
    w  v -u -t  s  r -q  p -o  n -m -l  k  j -i -1
"""

complex_abs_data = [
    [ [ 1, 2], sqrt(5 ) ],
    [ [ 3,-2], sqrt(13) ]
]

complex_add_data = [
    [ [ 1, 2], [ 3,-3], [ 4,-1] ],
    [ [ 3,-3], [ 1, 2], [ 4,-1] ]
]

complex_sub_data = [
    [ [ 1, 2], [ 3,-3], [-2, 5] ],
    [ [ 3,-3], [ 1, 2], [ 2,-5] ]
]

complex_product_data = [
    [ [ 1, 2], [ 3,-3], [ 9, 3] ],
    [ [ 3,-3], [ 1, 2], [ 9, 3] ]
]

complex_division_data = [
    [ [ 1, 2], [ 3,-3], [-1/6, 1/2] ],
    [ [ 3,-3], [ 1, 2], [-3/5,-9/5] ]
]

dual_abs_data = [
    [ [ 1, 2], 1 ],
    [ [ 3,-2], 3 ]
]

dual_add_data = [
    [ [ 1, 2], [ 3,-3], [ 4,-1] ],
    [ [ 3,-3], [ 1, 2], [ 4,-1] ]
]

dual_sub_data = [
    [ [ 1, 2], [ 3,-3], [-2, 5] ],
    [ [ 3,-3], [ 1, 2], [ 2,-5] ]
]

dual_product_data = [
    [ [ 1, 2], [ 3,-3], [ 3, 3] ],
    [ [ 3,-3], [ 1, 2], [ 3, 3] ]
]

dual_division_data = [
    [ [ 1, 2], [ 3,-3], [1/3, 1] ],
    [ [ 3,-3], [ 1, 2], [  3,-9] ]
]


# Data Generators...

complex_abs_record      = [ (Complex(a),expect)                for a,expect in complex_abs_data      ]
complex_add_record      = [ (Complex(a),Complex(b),Complex(c)) for a,b,c    in complex_add_data      ]
complex_sub_record      = [ (Complex(a),Complex(b),Complex(c)) for a,b,c    in complex_sub_data      ]
complex_product_record  = [ (Complex(a),Complex(b),Complex(c)) for a,b,c    in complex_product_data  ]
complex_division_record = [ (Complex(a),Complex(b),Complex(c)) for a,b,c    in complex_division_data ]
dual_abs_record         = [ (Dual(a),expect)                   for a,expect in dual_abs_data         ]
dual_add_record         = [ (Dual(a),Dual(b),Dual(c))          for a,b,c    in dual_add_data         ]
dual_sub_record         = [ (Dual(a),Dual(b),Dual(c))          for a,b,c    in dual_sub_data         ]
dual_product_record     = [ (Dual(a),Dual(b),Dual(c))          for a,b,c    in dual_product_data     ]
dual_division_record    = [ (Dual(a),Dual(b),Dual(c))          for a,b,c    in dual_division_data    ]


# Class tools...

def random_vector(obj):
    return obj([random() for i in range(dim(obj))])

def random_imaginary_vector(obj):
    return obj([0] + [random() for i in range(dim(obj)-1)])

def unit_list (obj):
    d = 2 ** len(obj.dp)
    return [ obj( ( [0]*i + [1] + [0]*(d-i-1) )) for i in range(d) ]

#def generate_table (obj):
    #"""create a multiplication table for a given Algebra object in n×n matrix format (n=dimensions)"""
    #units  = unit_list(obj)
    #return [ [j*i for i in units] for j in units]

#def generate_str (obj):
    #"""create a multiplication table for a given Algebra object and return the elements in string format"""
    #print('here')
    #units  = unit_list(obj)
    #print('here')
    #return [ [str(j*i) for i in units] for j in units]


def generate_str (obj):
    """create a multiplication table for a given Algebra object and return the elements in string format"""
    d = obj.dim(obj)
    units = [ obj( ( [zer]*i + [one] + [zer]*(d-i-1) )) for i in range(d) ]
    table = []
    raw_table = []
    for j in units:
        table.append([])
        raw_table.append([])
        for i in units:
            if DEBUG: raw_table[-1].append(str(j*i))
            table[-1].append(str(obj([c.name_in(s) for c in (j*i).state])))
            if DEBUG: print('{} × {} = {}'.format(j,i,j*i))
    return table
        

def dim (obj):
    """the expected number of dimensions given the number of doubling products of this object"""
    return 2**len(obj.dp)

def two_square_identity (x,y):
    a,b = x
    c,d = y
    return [a*c - d*b, d*a + b*c]

def four_square_identity (x,y):
    a,b,c,d = x
    e,f,g,h = y

    r = a*e - b*f - c*g - d*h
    s = a*f + b*e + c*h - d*g
    t = a*g - b*h + c*e + d*f
    u = a*h + b*g - c*f + d*e
    return [r,s,t,u]

def eight_square_identity (x,y):
    a,b,c,d,e,f,g,h = x
    i,j,k,l,m,n,o,p = y

    # assuming i^2 = -1 ...
    z1 = a*i - b*j - c*k - d*l - m*e - n*f - o*g - p*h
    z2 = a*j + b*i + c*l - d*k - m*f + n*e + o*h - p*g
    z3 = a*k - b*l + c*i + d*j - m*g - n*h + o*e + p*f
    z4 = a*l + b*k - c*j + d*i - m*h + n*g - o*f + p*e
    z5 = m*a - n*b - o*c - p*d + e*i + f*j + g*k + h*l
    z6 = m*b + n*a + o*d - p*c - e*j + f*i - g*l + h*k
    z7 = m*c - n*d + o*a + p*b - e*k + f*l + g*i - h*j
    z8 = m*d + n*c - o*b + p*a - e*l - f*k + g*j + h*i
    return [z1,z2,z3,z4,z5,z6,z7,z8]

# this was calculated by hand. There is a fair chance that it is wrong.
def sixteen_square_identity (x,y):
    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16 = x
    b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16 = y
    # assuming i^2 = -1 ...
    z1  = a1 * b1  - a2  * b2  - a3  * b3  - a4  * b4  - b5  * a5  - b6  * a6  - b7  * a7  - b8  * a8  - b9  * a9  - b10 * a10 - b11 * a11 - b12 * a12 - a13 * b13 - a14 * b14 - a15 * b15 - a16 * b16
    z2  = a1 * b2  + a2  * b1  + a3  * b4  - a4  * b3  - b5  * a6  + b6  * a5  + b7  * a8  - b8  * a7  - b9  * a10 + b10 * a9  + b11 * a12 - b12 * a11 - a13 * b14 + a14 * b13 + a15 * b16 - a16 * b15
    z3  = a1 * b3  - a2  * b4  + a3  * b1  + a4  * b2  - b5  * a7  - b6  * a8  + b7  * a5  + b8  * a6  - b9  * a11 - b10 * a12 + b11 * a9  + b12 * a10 - a13 * b15 - a14 * b16 + a15 * b13 + a16 * b14
    z4  = a1 * b4  + a2  * b3  - a3  * b2  + a4  * b1  - b5  * a8  + b6  * a7  - b7  * a6  + b8  * a5  - b9  * a12 + b10 * a11 - b11 * a10 + b12 * a9  - a13 * b16 + a14 * b15 - a15 * b14 + a16 * b13
    z5  = b5 * a1  - b6  * a2  - b7  * a3  - b8  * a4  + a5  * b1  + a6  * b2  + a7  * b3  + a8  * b4  - a13 * b9  - a14 * b10 - a15 * b11 - a16 * b12 + b13 * a9  + b14 * a10 + b15 * a11 + b16 * a12
    z6  = b5 * a2  + b6  * a1  + b7  * a4  - b8  * a3  - a5  * b2  + a6  * b1  - a7  * b4  + a8  * b3  + a13 * b10 - a14 * b9  + a15 * b12 - a16 * b11 - b13 * a10 + b14 * a9  - b15 * a12 + b16 * a11
    z7  = b5 * a3  - b6  * a4  + b7  * a1  + b8  * a2  - a5  * b3  + a6  * b4  + a7  * b1  - a8  * b2  + a13 * b11 - a14 * b12 - a15 * b9  + a16 * b10 - b13 * a11 + b14 * a12 + b15 * a9  - b16 * a10
    z8  = b5 * a4  + b6  * a3  - b7  * a2  + b8  * a1  - a5  * b4  - a6  * b3  + a7  * b2  + a8  * b1  + a13 * b12 + a14 * b11 - a15 * b10 - a16 * b9  - b13 * a12 - b14 * a11 + b15 * a10 + b16 * a9
    z9  = b9 * a1  - b10 * a2  - b11 * a3  - b12 * a4  - a5  * b13 - a6  * b14 - a7  * b15 - a8  * b16 + a9  * b1  + a10 * b2  + a11 * b3  + a12 * b4  + b5  * a13 + b6  * a14 + b7  * a15 + b8  * a16
    z10 = b9 * a2  + b10 * a1  + b11 * a4  - b12 * a3  - a5  * b14 + a6  * b13 + a7  * b16 - a8  * b15 - a9  * b2  + a10 * b1  - a11 * b4  + a12 * b3  + b5  * a14 - b6  * a13 - b7  * a16 + b8  * a15
    z11 = b9 * a3  - b10 * a4  + b11 * a1  + b12 * a2  - a5  * b15 - a6  * b16 + a7  * b13 + a8  * b14 - a9  * b3  + a10 * b4  + a11 * b1  - a12 * b2  + b5  * a15 + b6  * a16 - b7  * a13 - b8  * a14
    z12 = b9 * a4  + b10 * a3  - b11 * a2  + b12 * a1  - a5  * b16 + a6  * b15 - a7  * b14 + a8  * b13 - a9  * b4  - a10 * b3  + a11 * b2  + a12 * b1  + b5  * a16 - b6  * a15 + b7  * a14 - b8  * a13
    z13 = a5 * b9  - a6  * b10 - a7  * b11 - a8  * b12 + b13 * a1  + b14 * a2  + b15 * a3  + b16 * a4  - b5  * a9  + b6  * a10 + b7  * a11 + b8  * a12 + a13 * b1  - a14 * b2  - a15 * b3  - a16 * b4
    z14 = a5 * b10 + a6  * b9  + a7  * b12 - a8  * b11 - b13 * a2  + b14 * a1  - b15 * a4  + b16 * a3  - b5  * a10 - b6  * a9  - b7  * a12 + b8  * a11 + a13 * b2  + a14 * b1  + a15 * b4  - a16 * b3
    z15 = a5 * b11 - a6  * b12 + a7  * b9  + a8  * b10 - b13 * a3  + b14 * a4  + b15 * a1  - b16 * a2  - b5  * a11 + b6  * a12 - b7  * a9  - b8  * a10 + a13 * b3  - a14 * b4  + a15 * b1  + a16 * b2
    z16 = a5 * b12 + a6  * b11 - a7  * b10 + a8  * b9  - b13 * a4  - b14 * a3  + b15 * a2  + b16 * a1  - b5  * a12 - b6  * a11 + b7  * a10 - b8  * a9  + a13 * b4  + a14 * b3  - a15 * b2  + a16 * b1
    return [z1,z2,z3,z4,z5,z6,z7,z8,z9,z10,z11,z12,z13,z14,z15,z16]

# Verbose output formats

def _test_unit_multiplication (self,expect,calc):
    "generic unit product table"
    imaginaries = '1ijklmnopqrstuvw'
    #n  = 2**len(self.obj.dp)
    n  = self.obj.dim(self.obj)
    il = list(imaginaries[:n])

    if DEBUG: print("\ncalc:   {0}\nexpect: {1}\nil: {2}".format(calc, expect, il))

    if VERBOSE: 
        print(_verbose_unit_multiplication().format(
            object           = self.obj.__name__,
            expected_table   = pd.DataFrame( expect, index = il, columns = il ),
            calculated_table = pd.DataFrame(   calc, index = il, columns = il )
        ))
    self.assertListEqual(calc, expect)


def _verbose_unit_multiplication ():
   return """

=== expected {object} multiplication table ===

{expected_table}

=== calculated {object} multiplication table ===

{calculated_table}

...
"""

def _verbose_square_identity (*l):
   return """

=== {4} square identity test

Given:

       x: {0}

       y: {1}

These should be the same...

{4} identity test product is:

   formula(x × y):

      {2}

The involution product is:

   code(x × y):

      {3}
            """.format(*l)


def _claim_equal (calc,expect):
    print("""

These should be equal...

   calc = {0}
 expect = {1}

    """.format(calc,expect))


def _verbose_quaternion_metric_space ():
    return """

=== Quaternion Metric Space test

p1: {0}
q1: {1}
p2: {2}
q2: {3}
 a: {4}

These should be equal...

   calc = {5}
 expect = {6}
"""


def _verbose_quaternion_dot_product ():
    return """

=== Quaternion dot product test

Given:

      p: {0}
      q: {1}

then these should be equal...

  calc1: {2}
  calc2: {3}
 expect: {4}
"""


def _verbose_weak_alternative ():
    return """

=== {15} weak alternative condition test

Given:

           x  = {0}
           y  = {1}

These should{14} be equal...

 (y × x) × x  = {2}
 y ×(x  × x)  = {3}

These should{14} be equal...

 (x × y) × x  = {4}
  x ×(y  × x  = {5}

These should{14} be equal...

 (x × x) × y  = {6}
  x ×(x  × y) = {7}

These should{14} be equal...

 (x × y) × y  = {8}
  x ×(y  × y) = {9}

These should{14} be equal...

 (y × x) × y  = {10}
  y ×(x  × y) = {11}

These should{14} be equal...

 (y × y) × x  = {12}
  y ×(y  × x) = {13}
"""


def _verbose_diophantus ():
    return """

=== Diophantus (Brahmagupta-Fibonacci) Identity test

Given:

             x = {0}
             y = {1}

Having absolute values

        abs(x) = {2}
        abs(y) = {3}

These should{4} be equal...

 abs(x)×abs(y) = {5}
      abs(x×y) = {6}

"""


def _verbose_split_quaternion_nilpotent ():
    return """

=== Quaternion Nilpotent test

Given the nilpotent:

          q = {0}

verify it squares to zero:

        q×q = {1}
     expect = {2}
"""


def _verbose_split_quaternion_idempotent ():
    return """

=== Quaternion Idempotent test

Given the idempotent:

          q = {0}

...verify it squares to itself:

        q×q = {1}
     expect = {2}

"""


def _verbose_split_octonion_conjugation ():
    return """ 

=== Split Octonion Conjugation test

Comparing conjugate against this formula:

  conjugate(x) = -1/6*( x + (i*x)*i + (j*x)*j + (k*x)*k + (l*x)*l + (m*x)*m + (n*x)*n + (o*x)*o )
"""


def _verbose_octonion_conjugation ():
    return """ 

=== Octonion Conjugation test

Comparing conjugate against this formula:

  conjugate(x) = -1/6*( x + (i*x)*i + (j*x)*j + (k*x)*k + (l*x)*l + (m*x)*m + (n*x)*n + (o*x)*o )
"""


def _verbose_quaternion_conjugation ():
    return """ 

=== Quaternion Conjugation test

Comparing conjugate against this formula:

  conjugate(x) = -1/2*( x + (i*x)*i + (j*x)*j + (k*x)*k )
"""


def _verbose_commutative ():
    return """

=== {3} Commutative Property test

These should{0} be equal...

     x × y = {1}
     y × x = {2}
"""


def _verbose_moufang_condition ():
    return """

=== {12} Moufang Condition test

Given:

       x = {0}
       y = {1}
       z = {2}

These should{11} be equal...

  z × (x × (z × y)) = {3}
 ((z  × x) × z) × y = {4}

These should{11} be equal...

 x × (z × (y × z )) = {5}
 (( x × z) × y) × z = {6}

These should{11} be equal...

 (z × x) × (y × z ) = {7}
   (z × (x × y))× z = {8}

These should{11} be equal...

 (z × x) × (y × z ) = {9}
  z ×((x × y) × z ) = {10}
"""


def _verbose_power_associative ():
    return """

=== Power Associative tests

Given random unit vectors...

             x = {0}
             y = {1}
         x × y = {2}

Having a magnitude (abs) of 1...

        abs(x) = {3}
        abs(y) = {4}

Produce a product of magnitude 1...

    abs(x × y) = {5}

They should be in the same spot...

 distance to 1 = {6}
"""


def _verbose_split_quaternion_conjugate ():
    return """

=== Split Quaternion Conjugate test

Given:

 q = (a,b)
 q = ((w+zi),(y+xi))

Then:

 conj(x) × x = w² + x² - y² - z²
"""


def _debug_power_associative ():
    return """
       x: {0}
       y: {1}
   x × y: {2}
"""


# Classes

class TestComplex(unittest.TestCase):
    obj = Complex

    def test_unit_multiplication (self):
        "Complex number unit product table"
        expect = [ a.split() for a in complex_table.strip().split("\n") ]
        print('expect:',expect)
        calc = generate_str(self.obj)
        _test_unit_multiplication(self, expect=expect, calc=calc)

    def Xtest_abs_results (self):
        "various absolute results"
        for row in complex_abs_record:
            input, expect = row
            calc = abs(input)
            if DEBUG or VERBOSE:
                print("\n=== Complex Absolute Value tests")
                print("\n|{0}| =\nexpect = {1}\n  calc = {2}".format(input, expect, calc))
            self.assertEqual(calc, expect)

    def Xtest_add_results (self):
        "various addition results"
        for row in complex_add_record:
            a,b,expect = row
            calc = a+b
            if DEBUG or VERBOSE:
                print("\n=== Complex Addition tests")
                print("\n{0} + {1} =\nexpect = {2}\n  calc = {3}".format(a, b, expect, calc))
            self.assertEqual(expect,calc)
            self.assertIsInstance(expect, Complex)

    def Xtest_sub_results (self):
        "various subtraction results"
        for row in complex_sub_record:
            a,b,expect = row
            calc = a-b
            if DEBUG or VERBOSE:
                print("\n=== Complex Difference tests")
                print("\n{0} - {1} =\nexpect = {2}\n  calc = {3}".format(a, b, expect, calc))
            self.assertEqual(expect, calc)
            self.assertIsInstance(expect, Complex)

    def Xtest_product_results (self):
        "various product results"
        for row in complex_product_record:
            a,b,expect = row
            calc = a*b
            if DEBUG or VERBOSE:
                print("\n=== Complex Product tests")
                print("\n{0} × {1} =\nexpect = {2}\n  calc = {3}".format(a, b, expect, calc))
            self.assertEqual(expect, calc)
            self.assertIsInstance(expect, Complex)

    def Xtest_division_results (self):
        "various division results"
        for row in complex_division_record:
            a,b,expect = row
            calc = a/b
            if DEBUG or VERBOSE:
                print("\n=== Complex Division tests")
                print("\n{0} / {1} =\nexpect = {2}\n  calc = {3}".format(a, b, expect, calc))
            self.assertEqual(expect, calc)
            self.assertIsInstance(expect, Complex)


class TestDual(unittest.TestCase):

    """
Warning: there is a problem with this test.
The dual numbers do not all have absolute values.
So equality testing does not work.
Equality is based on distance between points.
So the distance between a & b = |a-b|
But since the absolute value of a dual number ignores the imaginary...
two dual numbers that have the same real value will have the same magnitude
regardless of the imaginary quantity.
It means that the dual class thinks (1,0) == (1,1000000)... which can not be right.
Should equality be forced to use pythagorus for distance calculations OR 
is that not allowed?
How can I tell if two dual numbers are so close they're probably be equal?
Until then, these tests are probably garbage.
    """

    obj = Dual

    def test_unit_multiplication (self):
        "Dual number unit product table"
        expect = [ a.split() for a in dual_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self, expect=expect, calc=calc)

    def Xtest_abs_results (self):
        "various absolute results"
        if DEBUG or VERBOSE:
            print()
        for row in dual_abs_record:
            input, expect = row
            calc = abs(input)
            if DEBUG or VERBOSE:
                print("\n=== Dual Absolute Value tests\n")
                print("|%s| =\nexpect = %s\n  calc = %s" % (input, expect, calc))
            self.assertEqual(calc, expect)

    def Xtest_add_results (self):
        "various addition results"
        if DEBUG or VERBOSE:
            print()
        for row in dual_add_record:
            a,b,expect = row
            calc = a+b
            if DEBUG or VERBOSE:
                print("\n=== Dual Addition tests\n")
                print("\n%s + %s =\nexpect = %s\n  calc = %s" % (a,b, expect, calc))
            self.assertEqual(expect,calc)
            self.assertIsInstance(expect, self.obj)

    def Xtest_sub_results (self):
        "various subtraction results"
        if DEBUG or VERBOSE:
            print()
        for row in dual_sub_record:
            a,b,expect = row
            calc = a-b
            if DEBUG or VERBOSE:
                print("\n=== Dual Difference tests\n")
                print("\n%s - %s =\nexpect = %s\n  calc = %s" % (a,b, expect, calc))
            self.assertEqual(expect,calc)
            self.assertIsInstance(expect, self.obj)

    def Xtest_product_results (self):
        "various product results"
        if DEBUG or VERBOSE:
            print()
        for row in dual_product_record:
            a,b,expect = row
            calc = a*b
            if DEBUG or VERBOSE:
                print("\n=== Dual Product tests\n")
                print("\n%s × %s =\nexpect = %s\n  calc = %s" % (a,b, expect, calc))
            self.assertEqual(expect,calc)
            self.assertIsInstance(expect, self.obj)

    def Xtest_division_results (self):
        "various division results"
        if DEBUG or VERBOSE:
            print()
        for row in dual_division_record:
            a,b,expect = row
            calc = a/b
            if DEBUG or VERBOSE:
                print("\n=== Dual Division tests\n")
                print("\n%s / %s =\nexpect = %s\n  calc = %s" % (a,b, expect, calc))
            self.assertEqual(expect,calc)
            self.assertIsInstance(expect, self.obj)


class TestSplit(unittest.TestCase):
    obj = Split

    def test_unit_multiplication (self):
        "Split number unit product table"
        expect = [ a.split() for a in split_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self, expect=expect, calc=calc)


class TestQuaternion(unittest.TestCase):
    obj = Quaternion

    def test_unit_multiplication (self):
        "Quaternion unit product table"
        expect      = [ a.split() for a in quaternion_table.strip().split("\n") ]
        calc        = generate_str(self.obj)
        _test_unit_multiplication(self, expect=expect, calc=calc)

    def Xtest_conjugation (self):
        "Long form congugation"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(self.obj)
            calc = x.conj()
            o,i,j,k = unit_list(self.obj)
            expect = -1/2*( x + (i*x)*i + (j*x)*j + (k*x)*k )
            if DEBUG:
                _claim_equal(repr(calc),repr(expect))
            self.assertEqual(calc,expect)
        if VERBOSE: 
            print(_verbose_quaternion_conjugation())
            _claim_equal(calc,expect)

    def Xtest_conjugate_product (self):
        "the product of a vector with its conjugate is the multidimensional Pythagarus formula"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
            print("\n=== Quaternion Conjugate Product test\n")
        for n in range(loops):
            x = random_vector(self.obj)
            calc = x*x.conj()
            expect = sum([a ** 2 for a in x])
            self.assertEqual(calc,expect)
        if DEBUG: 
            _claim_equal(repr(calc),repr(expect))
        if VERBOSE:
            _claim_equal(calc,expect)

    def Xtest_addition_metric_space (self):
        "Test addition is continuous in Quaternion metric topology"
        object = Quaternion
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            p1 = random_vector(self.obj)
            p2 = random_vector(self.obj)
            q1 = random_vector(self.obj)
            q2 = random_vector(self.obj)
            a  = uniform(0,10)
            calc   = abs((p1 + a*p2 + q1 + a*q2) - (p1+q1))
            expect = a*abs(p2+q2)
            if DEBUG:
                print(_verbose_quaternion_metric_space().format( p1, q1, p2, q2, a, repr(calc), repr(expect)))
            self.assertAlmostEqual(calc,expect)
        if VERBOSE:
            print(_verbose_quaternion_metric_space().format( p1, q1, p2, q2, a, repr(calc), repr(expect)))

    def Xtest_dot_product (self):
        "Component vs component free dot product"
        object = Quaternion
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            p = random_imaginary_vector(self.obj)
            q = random_imaginary_vector(self.obj)
            b1,c1,d1 = p[1:]
            b2,c2,d2 = q[1:]
            calc1 = 1/2*(p.conj()*q + q.conj()*p)
            calc2 = 1/2*(p*q.conj() + q*p.conj())
            expect = b1*b2 + c1*c2 + d1*d2
            if DEBUG:
                print(_verbose_quaternion_dot_product().format(p, q, calc1, calc2, expect))
            self.assertAlmostEqual(calc1,expect)
            self.assertAlmostEqual(calc2,expect)
            self.assertAlmostEqual(calc1,calc2)
        if VERBOSE:
            print(_verbose_quaternion_dot_product().format(p, q, calc1, calc2, expect))


class TestOctonion(unittest.TestCase):
    obj = Octonion

    def test_unit_multiplication (self):
        "Octonion unit product table"
        expect = [ a.split() for a in octonion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)

    def Xtest_conjugation (self):
        "Long form congugation"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(self.obj)
            calc = x.conj()
            o,i,j,k,l,m,n,o = unit_list(self.obj)
            expect = -1/6*( x + (i*x)*i + (j*x)*j + (k*x)*k + (l*x)*l + (m*x)*m + (n*x)*n + (o*x)*o )
            if DEBUG:
                print("   calc = %r" % (calc))
                print(" expect = %r" % (expect))
            self.assertEqual(calc,expect)
        if VERBOSE: 
            print(_verbose_octonion_conjugation())
            _claim_equal(calc,expect)

    def Xtest_conjugate_product (self):
        "the product of a vector with its conjugate is the multidimensional Pythagarus formula"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(self.obj)
            calc = x*x.conj()
            expect = sum([a ** 2 for a in x])
            self.assertEqual(calc,expect)
        if DEBUG: 
            _claim_equal(repr(calc),repr(expect))
        if VERBOSE:
            _claim_equal(calc,expect)


class TestSedenion(unittest.TestCase):
    obj = Sedenion

    def test_unit_multiplication (self):
        "Sedenion unit product table"
        expect = [ a.split() for a in sedenion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)


# Exotic Algebra tests

class TestSplitQuaternion(unittest.TestCase):
    obj = SplitQuaternion

    def test_unit_multiplication (self):
        "Split Quaternion unit product table"
        expect = [ a.split() for a in split_quaternion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)

    def Xtest_split_complex_generation (self):
        "Generation Split Quaternion from split-complex numbers"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        if DEBUG or VERBOSE: 
            print()
        for n in range(loops):
            q = random_vector(self.obj)
            a = Split(q[:2])
            b = Split(q[2:])
            w,z = a
            y,x = b
            pre_calc = w**2 + x**2 - y**2 - z**2
            calc = Split([pre_calc,0])
            expect = a*a.conj() - b*b.conj()
            if DEBUG:
                _claim_equal(repr(calc),repr(expect))
            self.assertEqual(calc,expect)
        if VERBOSE:
            print(_verbose_split_quaternion_conjugate())
            _claim_equal(calc,expect)

    def Xtest_nilpotent(self):
        "Test Split Quaternion nilpotent - a number whose square is zero"
        o,i,j,k = unit_list(self.obj)
        for unit in [-k, -j, k, j]:
            q = i-unit
            calc = q*q
            expect = self.obj([0,0,0,0])
            if VERBOSE:
                print(_verbose_split_quaternion_nilpotent().format(q, calc, expect))
            self.assertAlmostEqual(calc,expect)

    def Xtest_idempotent(self):
        "Test Split Quaternion nilpotent - a number whose square is zero"
        o,i,j,k = unit_list(self.obj)

        # todo: There must be more of these...

        q = 1/2*(o+j)
        calc = q*q
        expect = q
        if DEBUG:
            print("\n%8s = %r" % ('q',q))
            print("\n%8s = %r" % ('q×q',calc))
        if VERBOSE:
            print(_verbose_split_quaternion_idempotent().format(q, calc, expect))
        self.assertAlmostEqual(calc,expect)


class TestSplitOctonion(unittest.TestCase):
    obj = SplitOctonion

    def test_unit_multiplication (self):
        "SplitOctonion unit product table"
        expect = [ a.split() for a in split_octonion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)

    def Xtest_conjugation (self):
        "Long form congugation"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for _ in range(loops):
            z = random_vector(self.obj)
            calc = z.conj()
            x,i,j,k,l,m,n,o = unit_list(self.obj)
            expect = x*z[0] - i*z[1] - j*z[2] - k*z[3]- l*z[4] - m*z[5] - n*z[6] - o*z[7]
            if DEBUG:
                _claim_equal(repr(calc),repr(expect))
            self.assertEqual(calc,expect)
        if VERBOSE: 
            print(_verbose_split_octonion_conjugation())
            _claim_equal(calc,expect)

    def Xtest_conjugate_product (self):
        "the product of a vector with its conjugate is the multidimensional Pythagarus formula"
        loops = 100
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(self.obj)
            calc = x*x.conj()
            expect = sum([a ** 2 for a in x[:4]]) - sum([a ** 2 for a in x[4:]])
            self.assertEqual(calc,expect)
        if DEBUG: 
            _claim_equal(repr(calc),repr(expect))
        if VERBOSE:
            _claim_equal(calc,expect)


class TestDualComplex(unittest.TestCase):
    obj = DualComplex

    def test_unit_multiplication (self):
        "DualComplex unit product table"
        expect = [ a.split() for a in dual_complex_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)


class TestDualQuaternion(unittest.TestCase):
    obj = DualQuaternion

    def test_unit_multiplication (self):
        "DualQuaternion unit product table"
        expect = [ a.split() for a in dual_quaternion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)


class TestHyperbolicQuaternion(unittest.TestCase):
    obj = HyperbolicQuaternion

    def test_unit_multiplication (self):
        "HyperbolicQuaternion unit product table"
        expect = [ a.split() for a in hyperbolic_quaternion_table.strip().split("\n") ]
        calc = generate_str(self.obj)
        _test_unit_multiplication(self,expect=expect,calc=calc)


# Algebraic property tests

class Commutative():
    """Commutative Product tests"""

    def _is_commutative(self, obj, loops=100):
        d = dim(obj)
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(obj)
            y = random_vector(obj)
            x * y
            if d > 2:
                self.assertNotEqual(x*y,y*x)
            else:
                self.assertEqual(x*y,y*x)
        if DEBUG: 
            print("x × y = %r" % (x*y))
            print("y × x = %r" % (y*x))
        if VERBOSE:
            print(_verbose_commutative().format((' NOT' if d>2 else ''),x*y,y*x,obj.__name__))

    def test_complex(self):
        self._is_commutative(Complex, loops=5000)

    def test_quaternion(self):
        self._is_commutative(Quaternion, loops=1000)

    def test_octonion(self):
        self._is_commutative(Octonion, loops=300)

    def test_sedenion(self):
        self._is_commutative(Sedenion)

    def test_cd32(self):
        self._is_commutative(Cd32,loops=50)


class WeakAlternative():

    def _is_weak_alternative(self, obj, loops=100):
        "Weak Alternative Condition tests"
        d = dim(obj)
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(obj)
            y = random_vector(obj)
            if d < 16:
                self.assertEqual((y*x)*x, y*(x*x))
                self.assertEqual((x*y)*x, x*(y*x))
                self.assertEqual((x*x)*y, x*(x*y))
                self.assertEqual((x*y)*y, x*(y*y))
                self.assertEqual((y*x)*y, y*(x*y))
                self.assertEqual((y*y)*x, y*(y*x))
            else:
                self.assertEqual((x*y)*x, x*(y*x))
                self.assertEqual((y*x)*y, y*(x*y))
                self.assertNotEqual((y*x)*x, y*(x*x))
                self.assertNotEqual((x*x)*y, x*(x*y))
                self.assertNotEqual((x*y)*y, x*(y*y))
                self.assertNotEqual((y*y)*x, y*(y*x))
        if VERBOSE:
            print(_verbose_weak_alternative().format(x,y,(y*x)*x,y*(x*x),(x*y)*x,x*(y*x),(x*x)*y,x*(x*y),(x*y)*y,x*(y*y),(y*x)*y,y*(x*y),(y*y)*x,y*(y*x),(' NOT' if d>8 else ''),obj.__name__))

    def test_complex(self):
        self._is_weak_alternative(Complex,loops=1000)

    def test_quaternion(self):
        self._is_weak_alternative(Quaternion, loops=300)

    def test_octonion(self):
        self._is_weak_alternative(Octonion)

    def test_sedenion(self):
        self._is_weak_alternative(Sedenion,loops=15)

    def test_32ion(self):
        self._is_weak_alternative(Cd32,loops=10)


class DiophantusIdentity():
    """
    Diophantus identity test
    Brahmagupta–Fibonacci / Diophantus identity
    """

    def _is_diophantus_identity(self, obj, loops=100):
        "Diophantus identity test"
        PRECISION = 10**-9
        d = dim(obj)
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(obj)
            y = random_vector(obj)
            if d > 8:
                self.assertNotAlmostEqual(abs(x) * abs(y), abs(x*y), delta=PRECISION)
            else:
                self.assertAlmostEqual(abs(x) * abs(y), abs(x*y), delta=PRECISION)

        if VERBOSE:
            print(_verbose_diophantus().format(x,y,abs(x),abs(y),(' NOT' if d>8 else ''),abs(x)*abs(y),abs(x*y)))

    def test_complex(self):
        self._is_diophantus_identity(Complex,loops=20000)

    def test_quaternion(self):
        self._is_diophantus_identity(Quaternion, loops=1000)

    def test_octonion(self):
        self._is_diophantus_identity(Octonion, loops=1000)

    #def test_sedenion(self):
        #self._is_diophantus_identity(Sedenion,loops=300)

    #def test_32ion(self):
        #self._is_diophantus_identity(Cd32,loops=200)

    #def test_split_octonion(self):
        #self._is_diophantus_identity(SplitOctonion, loops=300)


class MoufangCondition():
    """Moufang condition tests"""

    def _is_moufang_condition(self, obj, loops=100):
        "Moufang condition tests"
        dm = dim(obj)
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(obj)
            y = random_vector(obj)
            z = random_vector(obj)
            a = z*(x*(z*y))
            b = ((z*x)*z)*y
            c = x*(z*(y*z))
            d = ((x*z)*y)*z
            e = (z*x)*(y*z)
            f = (z*(x*y))*z
            g = (z*x)*(y*z)
            h = z*((x*y)*z)
            if dm > 8:
                self.assertNotEqual(a,b)
                self.assertNotEqual(c,d)
                self.assertNotEqual(e,f)
                self.assertNotEqual(g,h)
            else:
                self.assertEqual(a,b)
                self.assertEqual(c,d)
                self.assertEqual(e,f)
                self.assertEqual(g,h)
        if DEBUG:
            print("%8s: %r\n" % ('x',x))
            print("%8s: %r\n" % ('y',y))
            print("%8s: %r\n" % ('z',z))
        if VERBOSE:
            a = z*(x*(z*y))
            b = ((z*x)*z)*y
            c = x*(z*(y*z))
            d = ((x*z)*y)*z
            e = (z*x)*(y*z)
            f = (z*(x*y))*z
            g = (z*x)*(y*z)
            h = z*((x*y)*z)
            print(_verbose_moufang_condition().format(x,y,z,a,b,c,d,e,f,g,h,' NOT' if dm>8 else '', obj.__name__))

    def test_complex(self):
        self._is_moufang_condition(Complex,loops=500)

    def test_quaternion(self):
        self._is_moufang_condition(Quaternion, loops=150)

    def test_octonion(self):
        self._is_moufang_condition(Octonion, loops=50)

    def test_sedenion(self):
        self._is_moufang_condition(Sedenion,loops=15)

    def test_32ion(self):
        self._is_moufang_condition(Cd32,loops=10)

    #def test_split_octonion(self):
        #self._is_moufang_condition(SplitOctonion, loops=300)


class PowerAssociative():
    """Power Associative tests"""

    def _is_power_associative(self, obj, loops=100):
        PRECISION = 10**-9
        d = dim(obj)
        if VERBOSE or DEBUG: 
            print(loops, 'loops')
        for n in range(loops):
            x = random_vector(obj).normalize()
            y = random_vector(obj).normalize()
            z = x * y
            self.assertAlmostEqual(abs(x),1,delta=PRECISION)
            self.assertAlmostEqual(abs(y),1,delta=PRECISION)
            if d > 8:
                # this logic is questionable!!!
                self.assertAlmostEqual(abs(z),1,delta=10**-1)
            else:
                self.assertAlmostEqual(abs(z),1,delta=PRECISION)
        if DEBUG or 1:
            print(_debug_power_associative().format(repr(x), repr(y), repr(x*y)))
            # why these don't work...
            #print(_debug_power_associative().format( tuple(repr(i) for i in (x,y,x*y)) ))
            #print(_debug_power_associative().format( tuple([repr(i) for i in (x,y,x*y)]) ))
            #print(_debug_power_associative().format( (repr(i) for i in (x,y,x*y)]) ))

        if VERBOSE:
            print( _verbose_power_associative().format(x,y,z,abs(x),abs(y),abs(z),abs(z)-1) )

    #def test_complex(self):
        #self._is_power_associative(Complex,loops=8000)

    #def test_quaternion(self):
        #self._is_power_associative(Quaternion, loops=2400)

    #def test_octonion(self):
        #self._is_power_associative(Octonion, loops=800)

    #def test_sedenion(self):
        #self._is_power_associative(Sedenion,loops=120)

    #def test_32ion(self):
        #self._is_power_associative(Cd32,loops=80)

    #def test_split_octonion(self):
        #self._is_power_associative(SplitOctonion, loops=300)


class TwoSquareIdentity():
    """Two square identity"""

    def test_two_square_identity(self):
        obj = Complex
        x = random_vector(obj)
        y = random_vector(obj)
        calc = x*y
        formula = obj(two_square_identity(x,y))
        self.assertEqual(formula, calc)
        if VERBOSE:
            print(_verbose_square_identity(x,y,formula,calc,"Brahmagupta-Fibonacci's Two"))


class FourSquareIdentity():
    """Four square identity"""

    def test_four_square_identity(self):
        obj = Quaternion
        x = random_vector(obj)
        y = random_vector(obj)
        calc = x*y
        formula = obj(four_square_identity(x,y))
        self.assertEqual(formula, calc)
        if VERBOSE:
            print(_verbose_square_identity(x,y,formula,calc,"Euler's Four"))


class EightSquareIdentity():
    """Eight square identity"""

    def test_eight_square_identity(self):
        obj = Octonion
        x = random_vector(obj)
        y = random_vector(obj)
        calc = x*y
        formula = obj(eight_square_identity(x,y))
        self.assertEqual(formula, calc)
        if VERBOSE:
            print(_verbose_square_identity(x,y,formula,calc,"Degen's Eight"))


class SixteenSquareIdentity():
    """Sixteen square identity"""

    def test_sixteen_square_identity(self):
        obj = Sedenion
        x = random_vector(obj)
        y = random_vector(obj)
        calc = x*y
        formula = obj(sixteen_square_identity(x,y))
        self.assertAlmostEqual(formula, calc)
        if VERBOSE:
            print(_verbose_square_identity(x,y,formula,calc,"Pfister's Sixteen"))


# run all tests on execute...

if __name__ == '__main__':

    unittest.main(verbosity=2)

