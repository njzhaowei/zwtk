# -*- coding: utf-8 -*-
import pytest
import time

import zwtk.comm as comm

def test_print_duration():
    @comm.print_duration
    def test_func():
        for i in range(3):
            time.sleep(1)
    test_func()
    assert 1
