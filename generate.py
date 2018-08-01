#!/usr/local/bin/python
# coding=utf-8

import math
import json
from __future__ import print_function

default_max_side = 100

class Triangle(object):
    def __init__(self,base,side1,side2,height):
        self.base = base
        self.side1 = side1
        self.side2 = side2
        self.height = height

    @property
    def area(self):
        return self.base * self.height / 2

    @property
    def type(self):
        if self.side1 == self.side2:
            return "isosceles"
        # Right here excludes cases where the base is the hypotenuse
        elif self.side1 == self.height or self.side2 == self.height:
            return "right"
        # Not quite technically correct (since right triangles will also be
        # scalene
        else: return "scalene" 

def hero_area(a, b, c):
    """returns area of triangle given three side lengths, using Heron's formula"""
    
    s = (a+b+c)/2.0 # semiperimeter

    if max(a,b,c) > s:
        return 0 # 0 area for impossible triangles

    return math.sqrt(s*(s-a)*(s-b)*(s-c))

def isinteger(x):
    """ check if a float is a whole number"""
    return math.floor(x) == x

def generate_triangles(callback, max_side=default_max_side):
    """
    Generates triangles with integer sides, integer height and integer area.
    
    Args:
        max_side: The maximum side length to generate up to
        callback: A callback function taking a Triangle object, which is applied
                  to each triangle generated

    Returns:
        Nothing (use the callback)
    """

    # Loop through a>b>c where:
    # 0 < a < max_side
    # a/2 < b ≤ a
    # [if b ≤ a/2, then 2b≤a. But then b+c≤2b≤a, contradiction triangle ineq]
    # a-b < c ≤ b
    # [if c ≤ a-b, then b+c≤a, contradicting triangle inequality]
    # [nb - using triangle inquality for 'real' triangles: b+c > a. b+c=a results in
    # a degenerate triangle]
    for a in range (1,max_side):
        for b in range (a/2,a+1):
            for c in range (a-b+1,b+1):
                sides = (a,b,c) # sides of the triangle
                area = hero_area(*sides) # area, from Heron's formula
                heights = (2*area/a,2*area/b,2*area/c) # Vertical heights from corresponding side
                
                #First check for integer area. NB does not guarantee integer height
                if area == 0 or not isinteger(area): continue

                #Cycle through potential bases, checking if we have an integer height
                for i, h in enumerate(heights):
                    if isinteger(h):  # woo, we have one
                        triangle = Triangle(
                                base = sides[i],
                                side1 = sides[(i+1)%3],
                                side2 = sides[(i+2)%3],
                                height = h)

                        callback(triangle)

def main():
    generate_triangles(lambda t: print(vars(t)))

if __name__ == "__main__":
    main()
