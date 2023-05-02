# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
from zwtk.fileutils import readjson
from zwtk.geoutils import *

BASEPTH = Path('./tests/data/geoutils')
TEMPPTH = Path('./tests/data/geoutils/tmp')

@pytest.mark.parametrize(
    's, r', (
        ('浙江省台州市国民经济和社会发展统计公报', 331000),
        ('浙江省杭州市国民经济和社会发展统计公报', 330100),
        ('浙江省国民经济和社会发展统计公报', 330000),
        ('北京市昌平区国民经济和社会发展统计公报', 110114),
        ('浙江省温州市鹿城区国民经济和社会发展统计公报', 330302),
        
    )
)
def test_address2adcode(s, r):
    codes = readjson( BASEPTH/'codetree.json' )
    o = address2adcode(s, codes)
    assert o == r
