#!/usr/bin/python3
import unittest
from sinary import *
from data import sinary_sides as ss

verbose=1

def labels(n):
    l = label_maker()
    return [ next(l) for i in range(n) ]

def label_maker():
    yield
    r=[Fraction(0,1)]
    yield r[0]
    while True:
        yield r[0] - 1
        rn = [r[0]]
        for n in r[1:]:
            m = (rn[-1]+n)/2
            yield m
            rn.extend((m,n))
        yield rn[-1]+1
        r = [rn[0]-1] + rn + [rn[-1]+1]

class SinaryTests(unittest.TestCase):

    def test_split_join(self):
        c = 2**10
        for a in range(c):
            s = Sinary(c)
            a,b = split(s.v)
            n = Sinary(join(a,b))
            self.assertEqual(s,n)
        if verbose or 1:
            msg = '\nSuccess: verified {} split and joined to itself.'
            print(msg.format(c))


    def Test_sinary_split(self):
        for k in ss.keys():
            self.assertEqual(ss[k],split(k))
        if verbose:
            msg = '\nSuccess: verified the split of the first {} sinary numbers.'
            print(msg.format(len(ss)))

    def test_compare(self):
        c = 2**6
        l = labels(c*c)
        for a in range(1,c):
            for b in range(1,c):
                self.assertEqual(le(a,b), l[a]<=l[b])
                self.assertEqual(lt(a,b), l[a]< l[b])
                self.assertEqual(gt(a,b), l[a]> l[b])
                self.assertEqual(ge(a,b), l[a]>=l[b])
                self.assertEqual(eq(a,b), l[a]==l[b])
                self.assertEqual(ne(a,b), l[a]!=l[b])
        if verbose:
            msg = '\nSuccess: {} comparisons le() "<=" between {} sinary numbers.'
            print(msg.format(6*c*c,c))


    def test_multiply(self):
        c = 2**3
        l = labels(c*c)
        for a in range(1,c):
            for b in range(1,c):
                self.assertEqual(l[mul(a,b)], l[a]*l[b])
        if verbose:
            msg = '\nSuccess: verified {} multiplication of {} numbers'
            print(msg.format(c*c,c))

    def test_addition(self):
        c = 2**4
        l = labels(c*c)
        for a in range(1,c):
            for b in range(1,c):
                self.assertEqual(l[add(a,b)], l[a]+l[b])
        if verbose:
            msg = '\nSuccess: verified {} additions of {} numbers'
            print(msg.format(c*c,c))

    def test_negate(self):
        c = 2**12
        l = labels(c)
        for a in range(1,c):
            self.assertEqual(l[neg(a)],-l[a])
        if verbose:
            msg = '\nSuccess: verified negation of {} numbers'
            print(msg.format(c))

    def Test_subtract(self):
        c = 2**5
        l = labels(c*c)
        for a in range(1,c):
            for b in range(1,c):
                self.assertEqual(l[sub(a,b)], l[a]-l[b])
                self.assertEqual(l[sub(b,a)], l[b]-l[a])
        if verbose:
            msg = '\nSuccess: verified {} subtractions of {} numbers'
            print(msg.format(c*c*2,c))


if __name__ == '__main__':
    unittest.main()
#   unittest.main(verbosity=2)

