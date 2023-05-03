# -*- coding: utf-8 -*-
import pytest

from zwtk.osutils import *

def test_run_shell():
    r = run_shell('dir', 'C:\\')
    assert len(r) != 0