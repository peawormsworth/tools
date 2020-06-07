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
    obj = Hyper

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

    def Test_quaternion_unit_multiplication (self):
        "Quaternion unit product table"
        expect      = [ a.split() for a in quaternion_table.strip().split("\n") ]

        imaginaries = '1ijklmnopqrstuvw'
        n  = 4
        il = list(imaginaries[:n])
        expected_table = pd.DataFrame( expect, index = il, columns = il )
        print('\net:\n',expected_table)
        calc = generate_str(self.obj)
        _test_unit_multiplication(self, expect=expect, calc=calc)

    def test_quaternion_table(self):
        days = 2
        c = create(days=days)
        cnt = 0

        o = Hyper(c[1],c[0],c[0],c[0])
        i = Hyper(c[0],c[1],c[0],c[0])
        j = Hyper(c[0],c[0],c[1],c[0])
        k = Hyper(c[0],c[0],c[0],c[1])

        self.assertEqual(o*o,o)
        self.assertEqual(o*i,i)
        self.assertEqual(o*j,j)
        self.assertEqual(o*k,k)
        self.assertEqual(i*o,i)
        self.assertEqual(i*i,-o)
        self.assertEqual(i*j,k)
        self.assertEqual(i*k,-j)
        self.assertEqual(j*o,j)
        self.assertEqual(j*i,-k)
        self.assertEqual(j*j,-o)
        self.assertEqual(j*k,i)
        self.assertEqual(k*o,k)
        self.assertEqual(k*i,j)
        self.assertEqual(k*j,-i)
        self.assertEqual(k*k,-o)
        print('\nsuccess: 16 quaternion multiplications')

    def test_curset_multiply(self):
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

    def test_hyper_conjugate(self):
        days = 4
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('Can not conjugate None')
                    continue
                ha = Hyper(c[a],c[b])
                expect = Hyper(c[a],-c[b])
                if v: print("check that conjugate({}) = {}".format(ha,expect))
                self.assertEqual(ha.conjugate(),expect)
                cnt += 1
        print('\nsuccess: {} conjugations'.format(cnt))

    def test_hyper_multiply(self):
        days = 2
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                for d in c.keys():
                    for e in c.keys():
                        if None in (a,b,d,e):
                            if v: print('{} * {} = ?. Can not multiply with None'.format((a,b),(d,e)))
                            continue
                        #a,b,d,e = c[a],c[b],c[d],c[e]
                        ha = Hyper(c[a],c[b])
                        hb = Hyper(c[d],c[e])
                        expect = Hyper(c[a]*c[d]-c[e].star()*c[b],c[e]*c[a]+c[b]*c[d].star())
                        if v: print("check that {} * {} = {}".format(ha,hb,expect))
                        product = ha * hb
                        #print(product,expect)
                        self.assertEqual(product,expect)
                        cnt += 1
        print('\nsuccess: {} multiplications'.format(cnt))

    def test_hyper_subtraction(self):
        days = 2
        c = create(days=days)
        cnt = 0
        #if v: print('\n'.join(str(x) for x in c.keys()))
        for a in c.keys():
            for b in c.keys():
                for d in c.keys():
                    for e in c.keys():
                        if None in (a,b,d,e):
                            if v: print('{} - {} = ?. Can not add to None'.format((a,b),(d,e)))
                            continue
                        ha = Hyper(c[a],c[b])
                        hb = Hyper(c[d],c[e])
                        expect = Hyper(c[a] - c[d], c[b] - c[e])
                        if a - d not in c or b - e not in c:
                            if v: print('{} - {} = {}, but {} is not in our list'.format(ha,hb,expect,expect))
                        else:
                            if v: print("check that {} - {} = {}".format(ha,hb,expect))
                            diff = ha - hb
                            self.assertEqual(diff,expect)
                            cnt += 1
                        #expect = Hyper(d - a, e - b)
                        expect = Hyper(c[d] - c[a], c[e] - c[b])
                        if d - a not in c or e - b not in c:
                            if v: print('{} - {} = {}, but {} is not in our list'.format(hb,ha,expect,expect))
                        else:
                            if v: print("check that {} - {} = {}".format(hb,ha,expect))
                            diff = hb - ha
                            self.assertEqual(diff,expect)
                            cnt += 1
        print('\nsuccess: {} subtractions'.format(cnt))

    def test_hyper_addition(self):
        days = 2
        c = create(days=days)
        cnt = 0
        if v: print('\n'.join(str(x) for x in c.keys()))
        for a in c.keys():
            for b in c.keys():
                for d in c.keys():
                    for e in c.keys():
                        if None in (a,b,d,e):
                            if v: print('{} + {} = ?. Can not add to None'.format((a,b),(d,e)))
                            continue
                        ha = Hyper(c[a],c[b])
                        hb = Hyper(c[d],c[e])
                        expect = Hyper(c[a] + c[d], c[b] + c[e])
                        if a + b not in c or b + e not in c:
                            if v: print('{} + {} = {}, but {} is not in our list'.format(ha,hb,expect,expect))
                            continue
                        if v: print("check that {} + {} = {}".format(ha,hb,expect))
                        self.assertEqual(ha + hb,expect)
                        cnt += 1
        print('\nsuccess: {} two dimensional additions'.format(cnt))

    def test_hyper_negate(self):
        days = 3
        cnt  = 0
        c = create(days=days)
        if v: print('\n'.join(str(x) for x in c.keys()))
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('Can not negate:',(a,b))
                    continue
                if v: print('check that -{} = {}'.format((a,b),(-a,-b)))
                expect =  Hyper(-c[a],-c[b])
                calc   = -Hyper( c[a], c[b])
                self.assertEqual(calc,expect)
                cnt += 1
        print('\nsuccess: {} hyper negations'.format(cnt))

    def test_addition(self):
        days = 4
        c = create(days=days)
        cnt = 0
        #if v: print('\n'.join(str(x) for x in c.keys()))
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
                #self.assertEqual(sum,Hyper.construct(expect))
                cnt += 1
        print('\nsuccess: {} additions'.format(cnt))

    def test_subtraction(self):
        days = 4
        c = create(days=days)
        if v: print('\n'.join(str(x) for x in c.keys()))
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

    def test_curset_compare(self):
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

    def test_curset_negate(self):
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
