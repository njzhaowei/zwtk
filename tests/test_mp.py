# -*- coding: utf-8 -*-
import pytest

from zwtk import mprocessing as mp
from zwtk.osutils import iswin

def multirun_cbfunc(s):
    return 'result: %s' % s

class TestMP:
    def test_multicmd(self):
        args = ['.', '/']
        if iswin():
            cmds = [['dir' , a] for a in args]
        else:
            cmds = [['ls', '-l', a] for a in args]
        r = mp.multiprocess_cmd(cmds)
        assert len(r) == len(args)

    def test_multirun(self):
        num = 10
        args = [(a,) for a in range(num)]
        r = mp.multiprocess_run(multirun_cbfunc, args)
        assert len(r) == num
