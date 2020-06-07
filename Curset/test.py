#!/usr/bin/python3
from tools import *
import unittest

v = False
v = True

class Tests(unittest.TestCase):
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
        if v: print('\n'.join(str(x) for x in c.keys()))
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
