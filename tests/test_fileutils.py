# -*- coding: utf-8 -*-
import pytest
import os
import struct
from pathlib import Path

from zwtk import dlso
from zwtk import fileutils

BASEPTH = Path('./tests/data/fileutils')
TEMPPTH = BASEPTH / 'tmp'

def setup_module():
    teardown_module()
    TEMPPTH.mkdir(parents=True, exist_ok=True)

def teardown_module():
    fileutils.rmdir(TEMPPTH)

def test_binfile():
    pth =TEMPPTH / 'binfile'
    arr = [10, 20, 30, 40, 92]
    dat = struct.pack('5B', *arr)
    fileutils.writebin(pth, dat)
    s = os.path.getsize(pth)
    d = fileutils.readbin(pth)
    a = struct.unpack('5B', d)
    assert s == len(arr) and len(dlso.listinter(arr, a)) == 5

def test_md5():
    md5 = fileutils.md5('docs/libdocs/pytest.pdf')
    assert md5 == 'd2e81dddfd92aa86233be7c18bf3b5d8'

def test_zip():
    r = fileutils.zip(BASEPTH / 'file1.txt',TEMPPTH / 'file1.zip', pwd='123')
    assert r and Path(TEMPPTH / 'file1.zip').stat().st_size > 0
    r = fileutils.zip(BASEPTH / 'dir1',TEMPPTH / 'dir1.zip', pwd='123')
    assert r and Path(TEMPPTH / 'dir1.zip').stat().st_size > 0
    r = fileutils.zip(BASEPTH / 'dir1',TEMPPTH / 'dir1 .zip', pwd='123')
    assert r and Path(TEMPPTH / 'dir1 .zip').stat().st_size > 0

def test_unzip():
    r = fileutils.unzip(TEMPPTH / 'dir1.zip', TEMPPTH / 'unzip1', pwd='123')
    assert r and os.listdir(TEMPPTH / 'unzip1')
    r = fileutils.unzip(TEMPPTH / 'dir1 .zip', TEMPPTH / 'unzip2', pwd='123')
    assert r and os.listdir(TEMPPTH / 'unzip2')