# -*- coding: utf-8 -*-
import pytest
import time

from zwtk.rand import *

def test_random_digits():
    r = random_digits(4)
    assert len(r)==4
