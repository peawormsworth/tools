#!/usr/bin/python3
from tools import *
import unittest
import pandas as pd

v = False
#v = True

class Tests(unittest.TestCase):

    def test_inversion(self):
        c = create()
        self.assertEqual(~c[   1],c[   1])
        self.assertEqual(~c[  -1],c[  -1])
        self.assertEqual(~c[  -2],c[-1/2])
        self.assertEqual(~c[-1/2],c[  -2])
        self.assertEqual(~c[ 1/2],c[   2])
        self.assertEqual(~c[   2],c[ 1/2])
        print('\nsuccess: 6 divisions')

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
