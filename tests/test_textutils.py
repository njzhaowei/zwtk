# -*- coding: utf-8 -*-
import pytest

from zwtk import textutils as tu

def test_is_chinese():
    assert tu.is_chinese('我') == True
    assert tu.is_chinese('A') == False
    assert tu.is_chinese('體') == True
    assert tu.is_chinese('一') == True

def test_hasdigit():
    assert tu.hasdigit('aaabb, 332 44 -adaf')
    assert not tu.hasdigit('aaabb,-adaf')

@pytest.mark.parametrize(
    'sentence, result', (
        ('  Zhaowei  is NO1, 一天吃 1 顿 ， 1 顿 吃 一 天 ', 'Zhaowei is NO1,一天吃1顿，1顿吃一天'),
    )
)
def test_rmexblank(sentence, result):
    out = tu.rmexblank(sentence)
    assert out == result

def test_replacesequence():
    ss = '   \t  \n   '
    replacements = tu.ReplaceSequence()\
        .append('\n', '\n\n')\
        .append('\t')\
        .append(r'^\\s+$')
    rs = replacements.replace(ss)
    assert rs == '     \n\n   '

def test_inner_trim():
    s = '   \tAAA BBB \n   '
    assert tu.inner_trim(s) == 'AAABBB'

def test_find_datestr():
    r = tu.find_datestr('http://abc/20201001/abc')
    assert len(r)==1 and r[0] == '2020-10-01'
    r = tu.find_datestr('http://abc/2020-10-01/abc')
    assert len(r)==1 and r[0] == '2020-10-01'
    r = tu.find_datestr('http://abc/202010/abc')
    assert len(r)==1 and r[0] == '2020-10'
    r = tu.find_datestr('http://abc/2020-10/abc')
    assert len(r)==1 and r[0] == '2020-10'
    r = tu.find_datestr('http://sjj.jcs.gov.cn/art/2020/10/6/art_42147_519877.html')
    assert len(r)==1 and r[0] == '2020-10-06'


    r = tu.find_datestr('http://abc/22020-10-01/abc')
    assert len(r)==0
    r = tu.find_datestr('http://abc/220201001/abc')
    assert len(r)==1 # TODO bug

    r = tu.find_datestr('http://www.jinhu.gov.cn/col/1185_833426/art/202010/1602578455967HsLIulTb.html')
    assert len(r)==1 and r[0] == '2020-10'

    r = tu.find_datestr('http://da.jiangsu.gov.cn/art/2020/1/15/art_65298_8910761.html')
    assert len(r)==1 and r[0] == '2020-01-15'

def test_similarity():
    r = tu.similarity('中西医结合治疗糖尿病的临床观察', '中西医结合治疗糖尿病的临床观察乙')
    assert r>0.8