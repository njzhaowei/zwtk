# -*- coding: utf-8 -*-
import pytest
from pathlib import Path

from zwtk import fileutils
from zwtk.config import Config

BASEPATH = Path('./tests/data/network')
TEMPPATH = BASEPATH / 'tmp'

def setup_module():
    teardown_module()
    TEMPPATH.mkdir(parents=True, exist_ok=True)

def teardown_module():
    fileutils.rmdir(TEMPPATH)

def test_config():
    cfg = Config(BASEPATH/'test_config.json', default={'fld0':123})
    assert cfg.fld0==123

def test_set():
    cfg = Config()
    cfg.set('fld0', 123)
    assert cfg.fld0==123

def test_has():
    cfg = Config(BASEPATH/'test_config.json')
    assert 'fld0' in cfg
    cfg.set('fld1', 123)
    assert 'fld1' in cfg
    assert 'fld2' not in cfg