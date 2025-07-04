"""
6.1010 Spring 2023
Lab10 Optional Practice Exercises: Match
"""

#!/usr/bin/env python3
import os
import practice
import types
import pickle
import hashlib
import pytest


TEST_DIRECTORY = os.path.dirname(__file__)

with open(os.path.join(TEST_DIRECTORY, 'test_inputs', 'hanson.txt'), 'rb') as f:
    hanson = f.read().decode('utf-8')

def _load_test_file(name):
    with open(os.path.join(TEST_DIRECTORY, 'test_outputs', name), 'rb') as f:
        return pickle.load(f)

def _check_pattern_results(pattern, text, expected):
    result = [pattern.match(text[ix:]) for ix in range(len(text))]
    exp = [x if x is None else x[2] for i, x in enumerate(_load_test_file(expected))]
    assert (result == exp)

def test0_dot():
    p = practice.Dot()
    assert (p.match('hello') == 'h')
    assert (p.match('ello') == 'e')
    assert (p.match('') == None)
    _check_pattern_results(p, hanson, 'hanson.match.dot.pickle')

def test1_verbatim():
    p = practice.Verbatim('cat')
    assert (p.match('cat') == 'cat')
    assert (p.match(' cat') == None)
    assert (p.match('ca') == None)
    _check_pattern_results(practice.Verbatim('Hanson'), hanson, 'hanson.match.ver.pickle')
    _check_pattern_results(practice.Verbatim('music'), hanson, 'hanson.match.ver2.pickle')

def test2_charfrom():
    p = practice.CharFrom('abc')
    assert (p.match('bacdef') == 'b')
    assert (p.match('acdef') == 'a')
    assert (p.match('cdef') == 'c')
    assert (p.match(' cabdef') == None)
    assert (p.match(' cabdef') == None)
    assert (p.match('defcab') == None)
    _check_pattern_results(practice.CharFrom('Hanson'), hanson, 'hanson.match.cf.pickle')
    _check_pattern_results(practice.CharFrom('music'), hanson, 'hanson.match.cf2.pickle')

def test3_digit():
    p = practice.Digit()
    assert p.match('') == None
    assert p.match('b0123456789') == None
    assert p.match('0123456789') == '0'
    assert p.match('123456789') == '1'
    assert p.match('23456789') == '2'
    assert p.match('3456789') == '3'
    assert p.match('456789') == '4'
    assert p.match('56789') == '5'
    assert p.match('6789') == '6'
    assert p.match('789') == '7'
    assert p.match('89') == '8'
    assert p.match('9') == '9'
    _check_pattern_results(p, hanson, 'hanson.match.digit.pickle')

def test4_sequence():
    p = practice.Sequence([practice.CharFrom('abc'), practice.CharFrom('df'), practice.Verbatim('e')])
    assert (p.match('bacdef') ==  None)
    assert (p.match('acdef') == None)
    assert (p.match('cdef') == 'cde')
    assert (p.match('def') == None)
    assert (p.match('ef') == None)
    assert (p.match('f') == None)
    _check_pattern_results(practice.Sequence([practice.Verbatim('at '), practice.CharFrom('rstlne')]), hanson, 'hanson.match.seq2.pickle')

def test5_alternatives():
    p = practice.Alternatives([practice.CharFrom('abc'), practice.CharFrom('df'), practice.Verbatim('e')])
    assert (p.match('bacz1d2ef') == 'b')
    assert (p.match('acz1d2ef') == 'a')
    assert (p.match('cz1d2ef') == 'c')
    assert (p.match('z1d2ef') == None)
    assert (p.match('1d2ef') == None)
    assert (p.match('d2ef') == 'd')
    assert (p.match('2ef') == None)
    assert (p.match('ef') == 'e')
    assert (p.match('f') == 'f')
    _check_pattern_results(practice.Alternatives([practice.CharFrom('Hanson '), practice.Verbatim('the')]), hanson, 'hanson.match.alt.pickle')

def test6_repeat():
    p = practice.Repeat(practice.Verbatim('cat'), 2, 4)
    assert (p.match('cat') == None)
    assert (p.match('catcat') == 'catcat')
    assert (p.match('atcat') == None)
    assert (p.match('catcatcatcatcat') == 'catcatcatcat')
    assert (p.match('tcatcatcatcat') == None)
    assert (p.match('catcatca') == 'catcat')
    assert (p.match('at') == None)
    _check_pattern_results(practice.Repeat(practice.CharFrom('abcdefghijklm'), 2, 4), hanson, 'hanson.match.rep.pickle')
    _check_pattern_results(practice.Repeat(practice.CharFrom('abcdefghijklm'), 2, 2), hanson, 'hanson.match.rep2.pickle')

def test7_number():
    p = practice.Number()
    assert p.match('b01234 56789.12') == None
    assert p.match('01234 56789.12') == '01234'
    assert p.match('1234 56789.12') == '1234'
    assert p.match('234 56789.12') == '234'
    assert p.match('34 56789.12') == '34'
    assert p.match('4 56789.12') == '4'
    assert p.match(' 56789.12') == None
    assert p.match('9.12') == '9'
    assert p.match('.12') == None
    assert p.match('12') == '12'
    assert p.match('2') == '2'
    _check_pattern_results(p, hanson, 'hanson.match.number.pickle')

def test8_star():
    p = practice.Star(practice.CharFrom('abc'))
    assert (p.match('bacdef') == 'bac')
    assert (p.match('acdef') == 'ac')
    assert (p.match('cdef') == 'c')
    assert (p.match('def') == '')
    assert (p.match('') == '')
    assert (p.match('ababababababababababababababababccccccccccccdef') == 'ababababababababababababababababcccccccccccc')
    _check_pattern_results(practice.Star(practice.CharFrom('music')), hanson, 'hanson.match.star2.pickle')


def test_integration0_date():
    p = _make_patterns()['date']
    assert (p.match('2018-12-05') == '2018-12-05')
    assert (p.match('2018-12-92') == None)
    assert (p.match('20181205') == None)
    _check_pattern_results(p, hanson, 'hanson.match.date.pickle')

def test_integration1_ip_address():
    p = _make_patterns()['ip']
    with open(os.path.join(TEST_DIRECTORY, 'test_inputs', 'ip.txt'), 'rb') as f:
        ip_text = f.read().decode('utf-8')
    _check_pattern_results(p, ip_text, 'ip.match.pickle')
    _check_pattern_results(p, hanson, 'hanson.match.ip.pickle')

def test_integration3_url():
    p = _make_patterns()['url']
    _check_pattern_results(p, hanson, 'hanson.match.url.pickle')

def _find_all_test(name):
    pattern = _make_patterns()[name]
    expected = _load_test_file('hanson.find_all.%s.pickle' % name)
    result = pattern.find_all(hanson)
    assert isinstance(result, types.GeneratorType)
    assert list(result) == expected

def test_last_find_all_1():
    _find_all_test('num')

def test_last_find_all_2():
    _find_all_test('digit')

def test_last_find_all_3():
    _find_all_test('date')

def test_last_find_all_4():
    _find_all_test('url')

def test_last_find_all_5():
    _find_all_test('ip')

def test_last_find_all_6():
    _find_all_test('hha')

def test_last_find_all_deffed():
    classes = [practice.Dot, practice.Verbatim, practice.CharFrom,
                practice.Star, practice.Sequence, practice.Alternatives, practice.Repeat]
    methods = set()
    for cls in classes:
        find_all = getattr(cls, 'find_all', None)
        assert find_all != None, 'find_all cannot be called from a %s object' % cls.__name__
        methods.add(find_all)
    assert len(methods) == 1, 'find_all is defined %d times (instead of once)' % len(methods)

def _make_patterns():
    # Hha, an test (non-overlapping)
    hha = practice.Sequence([practice.CharFrom('Hha'), practice.CharFrom('an')])

    # Date
    month = practice.Alternatives([
        practice.Sequence([
            practice.Verbatim('0'),
            practice.CharFrom('123456789')
        ]),
        practice.Sequence([
            practice.Verbatim('1'),
            practice.CharFrom('012')
        ]),
    ])
    day = practice.Alternatives([
        practice.Sequence([
            practice.Verbatim('0'),
            practice.CharFrom('123456789')
        ]),
        practice.Sequence([
            practice.CharFrom('12'),
            practice.Digit()
        ]),
        practice.Sequence([
            practice.CharFrom('3'),
            practice.CharFrom('01')
        ]),
    ])
    year = practice.Sequence([
        practice.Alternatives([
            practice.Verbatim('19'),
            practice.Verbatim('20'),
        ]),
        practice.Repeat(practice.Digit(), 2, 2)
    ])
    dash = practice.Verbatim('-')
    date = practice.Sequence([
        year, dash, month, dash, day
    ])

    # IP Address
    digits = practice.Repeat(practice.Digit(), 1, 3)
    first = practice.Repeat(practice.Sequence([digits, practice.Verbatim('.')]), 3, 3)
    ip = practice.Sequence([first, digits])

    # URL
    lowerletters = 'abcdefghijklmnopqrstuvwxyz'
    upperletters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    others = r'%_+~#=-.?&'
    protocol = practice.Sequence([
        practice.Alternatives([practice.Verbatim('http'), practice.Verbatim('https')]),
        practice.Verbatim('://'),
    ])
    startchar = practice.CharFrom(lowerletters+upperletters+digits)
    dot = practice.Verbatim('.')
    start = practice.Star(practice.Sequence([practice.Star(startchar), dot]))
    tld = practice.Repeat(practice.CharFrom(lowerletters), 2, 4)
    pathpiece = practice.Sequence([practice.Verbatim('/'),
                                practice.Star(practice.CharFrom(lowerletters+upperletters+digits+others))])
    path = practice.Star(pathpiece)
    url = practice.Sequence([protocol, start, tld, path])

    return {'num': practice.Number(), 'digit': practice.Digit(), 'date': date, 'url': url, 'ip': ip, 'hha': hha}


if __name__ == '__main__':
    pass
