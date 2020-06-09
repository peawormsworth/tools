#!/usr/bin/python3
from tools import *
import unittest
import pandas as pd

v = False
#v = True

quaternion_table = """
    1  i  j  k
    i -1  k -j
    j -k -1  i
    k  j -i -1
"""

if not v: print("v = False, set v = True for verbose mode")

def generate_str (obj):
    """create a multiplication table for a given Algebra object and return the elements in string format"""

    units  = unit_list(obj)
    print('units:',units)
    return [ [str(j*i) for i in units] for j in units]

def unit_list (obj):
    d = 4
    return [ obj( ( *[nil]*i + [pos] + [nil]*(d-i-1) )) for i in range(d) ]

def _test_unit_multiplication (self,expect,calc):
    "generic unit product table"

    imaginaries = '1ijklmnopqrstuvw'
    n  = 4
    il = list(imaginaries[:n])

    if v: print("\ncalc:   {0}\nexpect: {1}\nil: {2}".format(calc, expect, il))

    if v: 
        print(_verbose_unit_multiplication().format(
            object           = self.obj.__name__,
            expected_table   = pd.DataFrame( expect, index = il, columns = il ),
            calculated_table = pd.DataFrame(   calc, index = il, columns = il )
        ))
    self.assertListEqual(calc, expect)


def _verbose_unit_multiplication ():
   return """
=== Expected {object} table ===
{expected_table}
=== Calculated {object} table ===
{calculated_table}
...
"""

class Tests(unittest.TestCase):
    #obj = Hyper

    def test_inversion(self):
        c = create()
        self.assertEqual(~c[   1],c[   1])
        self.assertEqual(~c[  -1],c[  -1])
        self.assertEqual(~c[  -2],c[-1/2])
        self.assertEqual(~c[-1/2],c[  -2])
        self.assertEqual(~c[ 1/2],c[   2])
        self.assertEqual(~c[   2],c[ 1/2])
        print('\nsuccess: 6 divisions')

    def Test_division(self):
        days = 5
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b) or b == 0:
                    if v: print('{} / {} = ?. Can not divide'.format(a,b))
                    continue
                expect = a / b
                if expect not in c:
                    if v: print('{} / {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                    continue
                if v: print("check that {} / {} = {}".format(a,b,expect))
                quotient = c[a] / c[b]
                self.assertEqual(quotient, c[expect])
                cnt += 1
        print('\nsuccess: {} divisions'.format(cnt))

    def test_multiply(self):
        days = 4
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('{} * {} = ?. Can not multiply nan'.format(a,b))
                    continue
                expect = a * b
                if expect not in c:
                    if v: print('{} * {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                    continue
                if v: print("check that {} * {} = {}".format(a,b,expect))
                product = c[a] * c[b]
                self.assertEqual(product,c[expect])
                cnt += 1
        print('\nsuccess: {} multiplications'.format(cnt))

    def test_addition(self):
        days = 4
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('{} + {} = ?. Can not add to None'.format(a,b))
                    continue
                expect = a + b
                if expect not in c:
                    if v: print('{} + {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                    continue
                if v: print("check that {} + {} = {}".format(a,b,expect))
                sum = c[a] + c[b]
                self.assertEqual(sum,c[expect])

                cnt += 1
        print('\nsuccess: {} additions'.format(cnt))

    def test_subtraction(self):
        days = 4
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('{} + {} = ?. Can not add to None'.format(a,b))
                    continue
                if b < 0: continue
                expect = a - b
                if expect not in c:
                    if v: print('{} - {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                else:
                    diff = c[a] - c[b]
                    if v: print('check that {} - {} = {}'.format(a,b,expect))
                    self.assertEqual(diff,c[expect])
                    cnt += 1
                expect = b - a
                if expect not in c:
                    if v: print('{} - {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                else:
                    diff = c[b] - c[a]
                    if v: print('check that {} - {} = {}'.format(b,a,expect))
                    self.assertEqual(diff,c[expect])
                    cnt += 1
        print('\nsuccess: {} subtractions'.format(cnt))

    def test_compare(self):
        days = 5
        c = create(days=days)
        for a in c.keys():
            if a is None: continue
            for b in c.keys():
                if not (a and b): continue
                if v: print("check that {} <  {} is {}".format(a,b,a< b))
                #self.assertIs(lt(c[a],c[b]),a< b)
                self.assertIs(c[a]< c[b],a< b)
                if v: print("check that {} <= {} is {}".format(a,b,a<=b))
                self.assertIs(c[a]<=c[b],a<=b)
                if v: print("check that {} == {} is {}".format(a,b,a==b))
                self.assertIs(c[a]==c[b],a==b)
                if v: print("check that {} >= {} is {}".format(a,b,a>=b))
                self.assertIs(c[a]>=c[b],a>=b)
                if v: print("check that {} >  {} is {}".format(a,b,a> b))
                self.assertIs(c[a]> c[b],a> b)
                if v: print("check that {} != {} is {}".format(a,b,a!=b))
                self.assertIs(c[a]!=c[b],a!=b)
        print('\nsuccess: {} comparisons ({} elements in {} ways)'.format(7*len(c),len(c),7))

    def test_numeric(self):
        days = 7
        c = create(days=days)
        for a in c.keys():
            if not a: continue
            if v: print('check {} = {}'.format(a,c[a]))
            self.assertEqual(float(c[a]),float(a))
        print('\nsuccess: {} numeric evaluations'.format(2**days))

    def test_negate(self):
        days = 9
        cnt = 0
        c = create(days=days)
        for a in c.keys():
            if a is None: continue
            if v: print("check that -({}) = {}".format(a,-a))
            self.assertEqual(-c[a],c[-a])
            cnt += 1
        print('\nsuccess: {} negations'.format(cnt))

if __name__ == '__main__':
    unittest.main(verbosity=2)
