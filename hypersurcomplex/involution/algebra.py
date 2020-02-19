# -*- coding: utf-8 -*-
# $Id: involution/algebra.py $
# Author: Jeff Anderson <truejeffanderson@gmail.com>
# Copyright: AGPL

"""
involution.algebra

python class of algebriac types of involution.Algebra

source: https://github.com/peawormsworth
author: Jeffrey B Anderson - truejeffanderson at gmail.com
"""

from involution import Algebra

class Complex (Algebra):
    ii = '-'
    dp = '3'

class Dual (Algebra):
    ii = '0'
    dp = '3'

class Split (Algebra):
    """Split-complex numbers also knowns as real tessarines"""
    ii = '+'
    dp = '3'

class Quaternion (Algebra):
    ii = '--'
    dp = '34'

class Octonion (Algebra):
    ii = '---'
    dp = '334'

class Sedenion (Algebra):
    ii = '----'
    dp = '3334'

class SplitQuaternion (Algebra):
    """SplitQuaternion. aka: Para-quaternion, exspherical system, Antiquaternion, Pseudoquaternion"""
    ii = '-+'
    dp = '34'

class SplitOctonion (Algebra):
    ii = '--+'
    dp = '330'

class DualComplex (Algebra):
    ii = '-0'
    dp = '74'


### Half-tested: I think I am right but a reference says otherwise...

class HyperbolicQuaternion (Algebra):
    ## close...
    ii = '++'
    dp = '34'

class DualQuaternion (Algebra):
    ## close...
    ii = '--0'
    dp = '335'

#########################################
# Untested ...
#########################################

class Cd32 (Algebra):
    ii = '-----'
    dp = '33334'

class Cd64 (Algebra):
    ii = '------'
    dp = '333334'

class BiComplex            (Algebra): pass
# Tessarine = Bicomplex
class Tessarine            (BiComplex): pass
class BiQuaternion         (Algebra): pass
class BiOctonion           (Algebra): pass
class SplitBiQuaternion    (Algebra): pass
class MulticomplexNumber   (Algebra): pass
class Spacetime            (Algebra): pass


