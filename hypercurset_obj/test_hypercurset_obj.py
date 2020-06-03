#!/usr/bin/python3
from hypercurset_obj_tools import *
import unittest

v = False

class HyperCursetTests(unittest.TestCase):
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
                quotient= divide(c[a], c[b])
                self.assertTrue(eq(quotient, c[expect]))
                cnt += 1
        print('\nsuccess: {} divisions'.format(cnt))

    def test_curset_multiply(self):
        days = 5
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
                product = mul(c[a],c[b])
                self.assertTrue(eq(product,c[expect]))
                cnt += 1
        print('\nsuccess: {} multiplications'.format(cnt))

    def test_hyper_conjugate(self):
        days = 5
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('{} * {} = ?. Can not multiply with None'.format((a,b),(d,e)))
                    continue
                expect = HyperCurset(a,-b)
                ha = HyperCurset(a,b)
                if v: print("check that conj({}) = {}".format(ha,expect))
                self.assertTrue(eq(conj(ha),expect))
                cnt += 1
        print('\nsuccess: {} conjugations'.format(cnt))

    def test_hyper_multiply(self):
        days = 3
        c = create(days=days)
        cnt = 0
        for a in c.keys():
            for b in c.keys():
                for d in c.keys():
                    for e in c.keys():
                        if None in (a,b,d,e):
                            if v: print('{} * {} = ?. Can not multiply with None'.format((a,b),(d,e)))
                            continue
                        expect = HyperCurset(a*d-b*e,a*e+b*d)
                        #if a + b not in c or b + e not in c:
                            #if v: print('{} + {} = {}, but {} is not in our list'.format((a,b),(d,e),expect,expect))
                            #continue
                        if v: print("check that {} * {} = {}".format((a,b),(d,e),expect))
                        product = HyperCurset(a,b) * HyperCurset(d,e)
                        self.assertTrue(eq(product,expect))
                        cnt += 1
        print('\nsuccess: {} multiplications'.format(cnt))

    def test_hyper_subtraction(self):
        days = 3
        c = create(days=days)
        cnt = 0
        if v: print('\n'.join(str(x) for x in c.keys()))
        for a in c.keys():
            for b in c.keys():
                for d in c.keys():
                    for e in c.keys():
                        if None in (a,b,d,e):
                            if v: print('{} - {} = ?. Can not add to None'.format((a,b),(d,e)))
                            continue
                        expect = HyperCurset(a - d, b - e)
                        if a - d not in c or b - e not in c:
                            if v: print('{} - {} = {}, but {} is not in our list'.format((a,b),(d,e),expect,expect))
                        else:
                            if v: print("check that {} - {} = {}".format((a,b),(d,e),expect))
                            sum = HyperCurset(a,b) - HyperCurset(d,e)
                            self.assertTrue(eq(sum[0],expect[0]))
                            self.assertTrue(eq(sum[1],expect[1]))
                            cnt += 1
                        expect = HyperCurset(d - a, e - b)
                        if d - a not in c or e - b not in c:
                            if v: print('{} - {} = {}, but {} is not in our list'.format((d,e),(a,b),expect,expect))
                        else:
                            if v: print("check that {} - {} = {}".format((d,e),(a,b),expect))
                            sum = HyperCurset(d,e) - HyperCurset(a,b)
                            self.assertTrue(eq(sum[0],expect[0]))
                            self.assertTrue(eq(sum[1],expect[1]))
                            cnt += 1
        print('\nsuccess: {} subtractions'.format(cnt))

    def test_hyper_addition(self):
        days = 3
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
                        expect = HyperCurset(a + d, b + e)
                        if a + b not in c or b + e not in c:
                            if v: print('{} + {} = {}, but {} is not in our list'.format((a,b),(d,e),expect,expect))
                            continue
                        if v: print("check that {} + {} = {}".format((a,b),(d,e),expect))
                        sum = HyperCurset(a,b) + HyperCurset(d,e)
                        self.assertTrue(eq(sum[0],expect[0]))
                        self.assertTrue(eq(sum[1],expect[1]))
                        cnt += 1
        print('\nsuccess: {} two dimensional additions'.format(cnt))

    def test_hyper_negate(self):
        days = 5
        cnt  = 0
        c = create(days=days)
        if v: print('\n'.join(str(x) for x in c.keys()))
        for a in c.keys():
            for b in c.keys():
                if None in (a,b):
                    if v: print('Can not negate:',(a,b))
                    continue
                if v: print('check that -{} = {}'.format((a,b),(-a,-b)))
                expect =  HyperCurset(-a,-b)
                calc   = -HyperCurset(+a,+b)
                self.assertTrue(eq(calc,expect))
                cnt += 1
        print('\nsuccess: {} hyper negations'.format(cnt))

    def test_addition(self):
        days = 5
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
                sum = add(c[a],c[b])
                self.assertTrue(eq(sum,c[expect]))
                cnt += 1
        print('\nsuccess: {} additions'.format(cnt))

    def test_subtraction(self):
        days = 5
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
                    diff = sub(c[a],c[b])
                    if v: print('check that {} - {} = {}'.format(a,b,expect))
                    self.assertEqual(numeric(diff),expect)
                    cnt += 1
                expect = b - a
                if expect not in c:
                    if v: print('{} - {} = {}, but {} is not in our list'.format(a,b,expect,expect))
                else:
                    diff = sub(c[b],c[a])
                    if v: print('check that {} - {} = {}'.format(b,a,expect))
                    self.assertEqual(numeric(diff),expect)
                    cnt += 1
        print('\nsuccess: {} subtractions'.format(cnt))

    def test_curset_compare(self):
        days = 6
        c = create(days=days)
        for a in c.keys():
            if a is None: continue
            for b in c.keys():
                if None in (a,b): continue
                if v: print("check that {} <  {} is {}".format(a,b,a< b))
                self.assertIs(lt(c[a],c[b]),a< b)
                if v: print("check that {} <= {} is {}".format(a,b,a<=b))
                self.assertIs(le(c[a],c[b]),a<=b)
                if v: print("check that {} == {} is {}".format(a,b,a==b))
                self.assertIs(eq(c[a],c[b]),a==b)
                if v: print("check that {} >= {} is {}".format(a,b,a>=b))
                self.assertIs(ge(c[a],c[b]),a>=b)
                if v: print("check that {} >  {} is {}".format(a,b,a> b))
                self.assertIs(gt(c[a],c[b]),a> b)
        print('\nsuccess: {} comparisons ({} elements in {} ways)'.format(6*len(c),len(c),6))

    def test_numeric(self):
        days = 8
        c = create(days=days)
        for a in c.keys():
            if a is None: continue
            if v: print('check {} = {}'.format(a,c[a]))
            self.assertEqual(numeric(c[a]),a)
        print('\nsuccess: {} numeric evaluations'.format(2**days))

    def test_curset_negate(self):
        days = 8
        cnt = 0
        c = create(days=days)
        for a in c.keys():
            if a is None: continue
            if v: print("check that -({}) = {}".format(a,-a))
            self.assertTrue(eq(negate(c[a]),c[-a]))
            self.assertEqual(numeric(negate(c[a])),numeric(c[-a]))
            cnt += 1
        print('\nsuccess: {} negations, {} tests'.format(cnt, 2*cnt))

if __name__ == '__main__':
    unittest.main(verbosity=2)
