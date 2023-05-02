# -*- coding: utf-8 -*-
import pytest

from zwtk.urlutils import *

def test_urlutils():
    d = ('http://a.com/b?p1=1&p2=2', 'http://a.com/b')
    assert remove_args(d[0]) == d[1]

    d = ('http://a.com/b?url=http%3A%2F%2Fr.com', 'http://r.com')
    assert get_redirect(d[0]) == d[1]

    d = ('http://a.com/b', 'a.com')
    assert get_domain(d[0]) == d[1]

    d = ('http://a.com/b', 'http')
    assert get_scheme(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', '/b/c')
    assert get_path(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', True)
    assert is_abs_url(d[0]) == d[1]
    d = ('b/c?p1=1', False)
    assert is_abs_url(d[0]) == d[1]

    d = ('http://blahblah/images/car.jpg', 'jpg')
    assert url_to_filetype(d[0]) == d[1]

    d = ('http://a.com/b/c?p1=1', 'http://a.com')
    assert get_base(d[0]) == d[1]

    d = ('http://www.example.org/default.html?ct=32&op=92&item=98', {'item': '98', 'op': '92', 'ct': '32'})
    assert get_params(d[0]) == d[1]

    d = ('http://example.com/../thing///wrong/../multiple-slashes-yeah/.', 'http://example.com/thing///multiple-slashes-yeah/')
    assert resolve_url(d[0]) == d[1]

    d = ('http://blahblah/images/car.jpg', True)
    assert is_url_image(d[0]) == d[1]

    d = ( ['http://abc.yew.com', 'http://abc.def.yew.com'], 2)
    assert subdomain_compare(d[0][0], d[0][1]) == d[1]

    # hostip = ping('baidu.com')
    # d = ( 'https://www.baidu.com/', hostip)
    # assert domain2ip(d[0]) == d[1]
    # d = ( 'baidu.com', hostip)
    # assert domain2ip(d[0]) == d[1]

def test_slugify():
    s = slugify('UK vows action after record-high migrant crossing of Channel')
    assert s == 'uk-vows-action-after-record-high-migrant-crossing-of-channel'

    s = slugify('ABC 走向 我们的小康生活')
    assert s == 'abc-走向-我们的小康生活'