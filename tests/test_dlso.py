# -*- coding: utf-8 -*-
import pytest
import collections
import zwtk.dlso as dlso

def test_zwobject():
    o = dlso.ZWObject.from_dict({
        'flda': 'a',
        'fldb': 'b'
    })
    assert isinstance(o, collections.Iterable)
    arr = []
    for v in o:
        arr.append(v)
    assert sorted(arr) == ['a', 'b']
    # TODO
    assert 'a' in o
    assert not hasattr(o, '_keys')
    assert 'c' not in o
    assert not hasattr(o, '_keys')
    assert o.get('flda', 'c') == 'a' and o.get('fldc', 'c') == 'c'
    assert sorted(o.keys()) == ['flda', 'fldb']

# pylint: disable=no-member
def test_dict2obj():
    r = dlso.dict2obj({
        's': 's',
        'n': 1,
        'list': [1, '2'],
        'dict': {'a1':'a1', 'a2':'a2', 'sub1':{'b1':'b1'}},
        'none': None,
        'obj': type('', (), {'a3': 'a3', 'sub2': type('', (),{'b2':'b2'})()})(),
        'zwo': dlso.ZWObject.from_dict({'a4':'a4'}),
    })
    assert r.s == 's' and r.none == None
    assert r.dict.a1 == 'a1' and r.dict.sub1.b1 == 'b1'
    assert r.obj.a3 == 'a3' and r.obj.sub2.b2 == 'b2'

    r = dlso.dict2obj(None)
    zwo = dlso.ZWObject()
    assert dlso.getflds(r) == dlso.getflds(zwo)

def test_obj2dict():
    r = dlso.obj2dict(type('', (), {
        's': 's',
        'n': 1,
        'list': [1, '2'],
        'dict': {'a1':'a1', 'a2':'a2', 'sub1':{'b1':'b1'}},
        'none': None,
        'obj': type('', (), {'a3': 'a3', 'sub2': type('', (),{'b2':'b2'})()})(),
        'zwo': dlso.ZWObject.from_dict({'a4':'a4'}),
    })())
    assert r['s'] == 's' and r['none'] == None
    assert r['dict']['a1'] == 'a1' and r['dict']['sub1']['b1'] == 'b1'
    assert r['obj']['a3'] == 'a3' and r['obj']['sub2']['b2'] == 'b2'

def test_arrs2recs():
    recs = dlso.arrs2recs(['hdr_a','hdr_b'], [['a', 'b'], ['c', 'd']])
    assert recs == [{'hdr_a':'a', 'hdr_b':'b'}, {'hdr_a':'c', 'hdr_b':'d'}]

def test_extend_attrs():
    o = type('', (), {'a1':'a1', 'a2':'a2'})()
    o = dlso.extend_attrs(o, {'a2':'n2', 'b1':'b1', 'sub1': {'c1': 'c1'}})
    assert o.a1 == 'a1' and o.a2 == 'n2' and o.b1 == 'b1' and o.sub1.c1 == 'c1'

    o = dlso.extend_attrs(o, type('', (), {'b1':'nb1'})())
    assert o.b1 == 'nb1'

def test_update_attrs():
    o = type('', (), {'a1':'a1', 'a2':'a2'})()
    o = dlso.update_attrs(o, {'a2':'n2', 'b1':'b1', 'sub1': {'c1': 'c1'}})
    assert o.a1 == 'a1' and o.a2 == 'n2' and not hasattr(o, 'b1') and not hasattr(o, 'sub1')

    o = dlso.update_attrs(o, type('', (), {'a1':'n1', 'b1':'nb1'})())
    assert o.a1 == 'n1' and not hasattr(o, 'b1')

def test_upsert_config():
    pcfg = dlso.ZWObject.from_dict({'p1': 'p1', 'p2':'p2'})
    dcfg = {'p1': 'dp1', 'd1': 'd1', 'sub1': {'c1': 'c1'}}
    ncfg = {'p2': 'np2', 'd1': 'nd1', 'n1': 'n1'}
    acfg = {'a1': 'a1', 'n1': 'an1'}
    o = dlso.upsert_config(pcfg, dcfg, ncfg, acfg)
    assert id(o) == id(pcfg) and o.p1 == 'dp1' and o.p2 == 'np2' and o.d1 == 'nd1' and o.n1 == 'an1'
    assert o.sub1.c1 == 'c1'

def test_listinter():
    r = dlso.listinter([0,1,3,2], [2,3,4,5])
    assert set(r) == set([3,2])

def test_listsplit():
    r = dlso.listsplit(list(range(7)), 3)
    assert r == [ [0,1,2], [3,4,5], [6] ]

def test_listunify():
    r = dlso.listunify([{'a': 1}, {'a': 1}, {'a': 3}, {'b': 4}])
    assert r == [{'a': 1}, {'a': 3}, {'b': 4}]
    r = dlso.listunify([{'a': 1, 'b': 3}, {'a': 2, 'b': 3}, {'a': 3}, {'b': 4}], keyfunc=lambda x, y: 'b' in y and y['b'] not in {o['b'] for o in x} )
    assert r == [{'a': 1, 'b': 3}, {'b': 4}]

def test_listcmp():
    assert False == dlso.listcmp([1,2,3,3], [1,2,2,3])
    assert True == dlso.listcmp([1,2,3], [2,1,3])

def test_as_dict():
    obj = {
        'a1': 'a1',
        'a2': 2,
        'dictobj': {
            'df1': 1,
            'df2': 'b'
        }
    }
    o = dlso.ZWObject.from_dict(obj)
    assert o.as_dict() == obj

def test_list_groupby():
    arr = [
        {'flda':'a', 'fld':'a'},
        {'flda':'b', 'fld':'a'},
        {'flda':'b', 'fld':'b'},
    ]
    r = dlso.listgroupby(arr, 'fld')
    assert r[0] == ('a', [{'flda': 'a', 'fld': 'a'}, {'flda': 'b', 'fld': 'a'}])
    assert r[1] == ('b', [{'flda': 'b', 'fld': 'b'}])
