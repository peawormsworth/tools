#!/usr/bin/python3

import matplotlib.pyplot as plt
from random import random

def three_point_circle(z1,z2,z3):
    a = 1j*(z1-z2)
    b = 1j*(z3-z2)
    if a.real:
        m1 = a.imag/a.real
        c = (z1-z2)/2
        p1 = z2+c
        b1 = p1.imag-m1*p1.real
    if b.real:
        m2 = b.imag/b.real
        d = (z3-z2)/2
        p2 = z2+d
        b2 = p2.imag-m2*p2.real
    if a.real and b.real:
        x = (b2-b1)/(m1-m2)
        y = (m2*b1-m1*b2)/(m2-m1)
    elif a.real:
        x,y = 0,b1
    elif b.real:
        x,y = 0,b2
    else:
        x,y = 0,0
    center = x+1j*y
    radius = abs(center-z1)
    return x,y,radius

fig = plt.figure()
for n in range(3):
    points = ([random()+random()*1j for i in range(3)])
    h,v,radius = three_point_circle(*points)
    for i in range(3):
        plt.scatter( points[i].real,points[i].imag, s=5, c='black')
    x,y = [],[]
    poly = 128
    for i in range(poly):
        z = radius*1j**(i*4/poly)
        x.append(h+z.real)
        y.append(v+z.imag)
    plt.plot(x,y,c='lightgrey')
plt.show()





