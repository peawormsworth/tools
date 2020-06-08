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
        print('\nsuccess: 16 quaternion unit multiplications')

    def test_octonion_table(self):
        days = 2
        c = create(days=days)
        cnt = 0

        x = Hyper(c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        i = Hyper(c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0])
        j = Hyper(c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0])
        k = Hyper(c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0])
        l = Hyper(c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0])
        m = Hyper(c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0])
        n = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0])
        o = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1])

        self.assertEqual(x*x,x)
        self.assertEqual(x*i,i)
        self.assertEqual(x*j,j)
        self.assertEqual(x*k,k)
        self.assertEqual(x*l,l)
        self.assertEqual(x*m,m)
        self.assertEqual(x*n,n)
        self.assertEqual(x*o,o)
        self.assertEqual(i*x,i)
        self.assertEqual(i*i,-x)
        self.assertEqual(i*j,k)
        self.assertEqual(i*k,-j)
        self.assertEqual(i*l,m)
        self.assertEqual(i*m,-l)
        self.assertEqual(i*n,-o)
        self.assertEqual(i*o,n)
        self.assertEqual(j*x,j)
        self.assertEqual(j*i,-k)
        self.assertEqual(j*j,-x)
        self.assertEqual(j*k,i)
        self.assertEqual(j*l,n)
        self.assertEqual(j*m,o)
        self.assertEqual(j*n,-l)
        self.assertEqual(j*o,-m)
        self.assertEqual(k*x,k)
        self.assertEqual(k*i,j)
        self.assertEqual(k*j,-i)
        self.assertEqual(k*k,-x)
        self.assertEqual(k*l,o)
        self.assertEqual(k*m,-n)
        self.assertEqual(k*n,m)
        self.assertEqual(k*o,-l)
        self.assertEqual(l*x,l)
        self.assertEqual(l*i,-m)
        self.assertEqual(l*j,-n)
        self.assertEqual(l*k,-o)
        self.assertEqual(l*l,-x)
        self.assertEqual(l*m,i)
        self.assertEqual(l*n,j)
        self.assertEqual(l*o,k)
        self.assertEqual(m*x,m)
        self.assertEqual(m*i,l)
        self.assertEqual(m*j,-o)
        self.assertEqual(m*k,n)
        self.assertEqual(m*l,-i)
        self.assertEqual(m*m,-x)
        self.assertEqual(m*n,-k)
        self.assertEqual(m*o,j)
        self.assertEqual(n*x,n)
        self.assertEqual(n*i,o)
        self.assertEqual(n*j,l)
        self.assertEqual(n*k,-m)
        self.assertEqual(n*l,-j)
        self.assertEqual(n*m,k)
        self.assertEqual(n*n,-x)
        self.assertEqual(n*o,-i)
        self.assertEqual(o*x,o)
        self.assertEqual(o*i,-n)
        self.assertEqual(o*j,m)
        self.assertEqual(o*k,l)
        self.assertEqual(o*l,-k)
        self.assertEqual(o*m,-j)
        self.assertEqual(o*n,i)
        self.assertEqual(o*o,-x)
        print('\nsuccess: 64 octonion unit multiplications')

    def test_sedenion_table(self):
        days = 2
        c = create(days=days)
        cnt = 0

        x = Hyper(c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        i = Hyper(c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        j = Hyper(c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        k = Hyper(c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        l = Hyper(c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        m = Hyper(c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        n = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        o = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        p = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0],c[0])
        q = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0],c[0])
        r = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0],c[0])
        s = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0],c[0])
        t = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0],c[0])
        u = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0],c[0])
        v = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1],c[0])
        w = Hyper(c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[0],c[1])

        self.assertEqual(x*x,x)
        self.assertEqual(x*i,i)
        self.assertEqual(x*j,j)
        self.assertEqual(x*k,k)
        self.assertEqual(x*l,l)
        self.assertEqual(x*m,m)
        self.assertEqual(x*n,n)
        self.assertEqual(x*o,o)
        self.assertEqual(x*p,p)
        self.assertEqual(x*q,q)
        self.assertEqual(x*r,r)
        self.assertEqual(x*s,s)
        self.assertEqual(x*t,t)
        self.assertEqual(x*u,u)
        self.assertEqual(x*v,v)
        self.assertEqual(x*w,w)

        self.assertEqual(i*x,i)
        self.assertEqual(i*i,-x)
        self.assertEqual(i*j,k)
        self.assertEqual(i*k,-j)
        self.assertEqual(i*l,m)
        self.assertEqual(i*m,-l)
        self.assertEqual(i*n,-o)
        self.assertEqual(i*o,n)
        self.assertEqual(i*p,q)
        self.assertEqual(i*q,-p)
        self.assertEqual(i*r,-s)
        self.assertEqual(i*s,r)
        self.assertEqual(i*t,-u)
        self.assertEqual(i*u,t)
        self.assertEqual(i*v,w)
        self.assertEqual(i*w,-v)

        self.assertEqual(j*x,j)
        self.assertEqual(j*i,-k)
        self.assertEqual(j*j,-x)
        self.assertEqual(j*k,i)
        self.assertEqual(j*l,n)
        self.assertEqual(j*m,o)
        self.assertEqual(j*n,-l)
        self.assertEqual(j*o,-m)
        self.assertEqual(j*p,r)
        self.assertEqual(j*q,s)
        self.assertEqual(j*r,-p)
        self.assertEqual(j*s,-q)
        self.assertEqual(j*t,-v)
        self.assertEqual(j*u,-w)
        self.assertEqual(j*v,t)
        self.assertEqual(j*w,u)

        self.assertEqual(k*x,k)
        self.assertEqual(k*i,j)
        self.assertEqual(k*j,-i)
        self.assertEqual(k*k,-x)
        self.assertEqual(k*l,o)
        self.assertEqual(k*m,-n)
        self.assertEqual(k*n,m)
        self.assertEqual(k*o,-l)
        self.assertEqual(k*p,s)
        self.assertEqual(k*q,-r)
        self.assertEqual(k*r,q)
        self.assertEqual(k*s,-p)
        self.assertEqual(k*t,-w)
        self.assertEqual(k*u,v)
        self.assertEqual(k*v,-u)
        self.assertEqual(k*w,t)

        self.assertEqual(l*x,l)
        self.assertEqual(l*i,-m)
        self.assertEqual(l*j,-n)
        self.assertEqual(l*k,-o)
        self.assertEqual(l*l,-x)
        self.assertEqual(l*m,i)
        self.assertEqual(l*n,j)
        self.assertEqual(l*o,k)
        self.assertEqual(l*p,t)
        self.assertEqual(l*q,u)
        self.assertEqual(l*r,v)
        self.assertEqual(l*s,w)
        self.assertEqual(l*t,-p)
        self.assertEqual(l*u,-q)
        self.assertEqual(l*v,-r)
        self.assertEqual(l*w,-s)

        self.assertEqual(m*x,m)
        self.assertEqual(m*i,l)
        self.assertEqual(m*j,-o)
        self.assertEqual(m*k,n)
        self.assertEqual(m*l,-i)
        self.assertEqual(m*m,-x)
        self.assertEqual(m*n,-k)
        self.assertEqual(m*o,j)
        self.assertEqual(m*p,u)
        self.assertEqual(m*q,-t)
        self.assertEqual(m*r,w)
        self.assertEqual(m*s,-v)
        self.assertEqual(m*t,q)
        self.assertEqual(m*u,-p)
        self.assertEqual(m*v,s)
        self.assertEqual(m*w,-r)

        self.assertEqual(n*x,n)
        self.assertEqual(n*i,o)
        self.assertEqual(n*j,l)
        self.assertEqual(n*k,-m)
        self.assertEqual(n*l,-j)
        self.assertEqual(n*m,k)
        self.assertEqual(n*n,-x)
        self.assertEqual(n*o,-i)
        self.assertEqual(n*p,v)
        self.assertEqual(n*q,-w)
        self.assertEqual(n*r,-t)
        self.assertEqual(n*s,u)
        self.assertEqual(n*t,r)
        self.assertEqual(n*u,-s)
        self.assertEqual(n*v,-p)
        self.assertEqual(n*w,q)

        self.assertEqual(o*x,o)
        self.assertEqual(o*i,-n)
        self.assertEqual(o*j,m)
        self.assertEqual(o*k,l)
        self.assertEqual(o*l,-k)
        self.assertEqual(o*m,-j)
        self.assertEqual(o*n,i)
        self.assertEqual(o*o,-x)
        self.assertEqual(o*p,w)
        self.assertEqual(o*q,v)
        self.assertEqual(o*r,-u)
        self.assertEqual(o*s,-t)
        self.assertEqual(o*t,s)
        self.assertEqual(o*u,r)
        self.assertEqual(o*v,-q)
        self.assertEqual(o*w,-p)

        self.assertEqual(p*x,p)
        self.assertEqual(p*i,-q)
        self.assertEqual(p*j,-r)
        self.assertEqual(p*k,-s)
        self.assertEqual(p*l,-t)
        self.assertEqual(p*m,-u)
        self.assertEqual(p*n,-v)
        self.assertEqual(p*o,-w)
        self.assertEqual(p*p,-x)
        self.assertEqual(p*q,i)
        self.assertEqual(p*r,j)
        self.assertEqual(p*s,k)
        self.assertEqual(p*t,l)
        self.assertEqual(p*u,m)
        self.assertEqual(p*v,n)
        self.assertEqual(p*w,o)

        self.assertEqual(q*x,q)
        self.assertEqual(q*i,p)
        self.assertEqual(q*j,-s)
        self.assertEqual(q*k,r)
        self.assertEqual(q*l,-u)
        self.assertEqual(q*m,t)
        self.assertEqual(q*n,w)
        self.assertEqual(q*o,-v)
        self.assertEqual(q*p,-i)
        self.assertEqual(q*q,-x)
        self.assertEqual(q*r,-k)
        self.assertEqual(q*s,j)
        self.assertEqual(q*t,-m)
        self.assertEqual(q*u,l)
        self.assertEqual(q*v,o)
        self.assertEqual(q*w,-n)

        self.assertEqual(r*x,r)
        self.assertEqual(r*i,s)
        self.assertEqual(r*j,p)
        self.assertEqual(r*k,-q)
        self.assertEqual(r*l,-v)
        self.assertEqual(r*m,-w)
        self.assertEqual(r*n,t)
        self.assertEqual(r*o,u)
        self.assertEqual(r*p,-j)
        self.assertEqual(r*q,k)
        self.assertEqual(r*r,-x)
        self.assertEqual(r*s,-i)
        self.assertEqual(r*t,-n)
        self.assertEqual(r*u,-o)
        self.assertEqual(r*v,l)
        self.assertEqual(r*w,m)

        self.assertEqual(s*x,s)
        self.assertEqual(s*i,-r)
        self.assertEqual(s*j,q)
        self.assertEqual(s*k,p)
        self.assertEqual(s*l,-w)
        self.assertEqual(s*m,v)
        self.assertEqual(s*n,-u)
        self.assertEqual(s*o,t)
        self.assertEqual(s*p,-k)
        self.assertEqual(s*q,-j)
        self.assertEqual(s*r,i)
        self.assertEqual(s*s,-x)
        self.assertEqual(s*t,-o)
        self.assertEqual(s*u,n)
        self.assertEqual(s*v,-m)
        self.assertEqual(s*w,l)

        self.assertEqual(t*x,t)
        self.assertEqual(t*i,u)
        self.assertEqual(t*j,v)
        self.assertEqual(t*k,w)
        self.assertEqual(t*l,p)
        self.assertEqual(t*m,-q)
        self.assertEqual(t*n,-r)
        self.assertEqual(t*o,-s)
        self.assertEqual(t*p,-l)
        self.assertEqual(t*q,m)
        self.assertEqual(t*r,n)
        self.assertEqual(t*s,o)
        self.assertEqual(t*t,-x)
        self.assertEqual(t*u,-i)
        self.assertEqual(t*v,-j)
        self.assertEqual(t*w,-k)

        self.assertEqual(u*x,u)
        self.assertEqual(u*i,-t)
        self.assertEqual(u*j,w)
        self.assertEqual(u*k,-v)
        self.assertEqual(u*l,q)
        self.assertEqual(u*m,p)
        self.assertEqual(u*n,s)
        self.assertEqual(u*o,-r)
        self.assertEqual(u*p,-m)
        self.assertEqual(u*q,-l)
        self.assertEqual(u*r,o)
        self.assertEqual(u*s,-n)
        self.assertEqual(u*t,i)
        self.assertEqual(u*u,-x)
        self.assertEqual(u*v,k)
        self.assertEqual(u*w,-j)

        self.assertEqual(v*x,v)
        self.assertEqual(v*i,-w)
        self.assertEqual(v*j,-t)
        self.assertEqual(v*k,u)
        self.assertEqual(v*l,r)
        self.assertEqual(v*m,-s)
        self.assertEqual(v*n,p)
        self.assertEqual(v*o,q)
        self.assertEqual(v*p,-n)
        self.assertEqual(v*q,-o)
        self.assertEqual(v*r,-l)
        self.assertEqual(v*s,m)
        self.assertEqual(v*t,j)
        self.assertEqual(v*u,-k)
        self.assertEqual(v*v,-x)
        self.assertEqual(v*w,i)

        self.assertEqual(w*x,w)
        self.assertEqual(w*i,v)
        self.assertEqual(w*j,-u)
        self.assertEqual(w*k,-t)
        self.assertEqual(w*l,s)
        self.assertEqual(w*m,r)
        self.assertEqual(w*n,-q)
        self.assertEqual(w*o,p)
        self.assertEqual(w*p,-o)
        self.assertEqual(w*q,n)
        self.assertEqual(w*r,-m)
        self.assertEqual(w*s,-l)
        self.assertEqual(w*t,k)
        self.assertEqual(w*u,j)
        self.assertEqual(w*v,-i)
        self.assertEqual(w*w,-x)

        print('\nsuccess: 256 sedenion unit multiplications')

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
        print('\nsuccess: {} complex additions'.format(cnt))

    def test_hyper_negate(self):
        days = 3
        cnt  = 0
        c = create(days=days)
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
