'''
6.101 Recipes Optional Practice Exercise
Refactory - Recursion part 1
'''

#!/usr/bin/env python3
import os
import pickle
import random
import pytest

import practice

TEST_DIRECTORY = os.path.dirname(__file__)


def setup_module(module):
    """
    This function loads the various databases.  It will be run once every time
    test.py is invoked.
    """
    filename = os.path.join(
        TEST_DIRECTORY,
        'resources',
        'tests.pickle')
    with open(filename, 'rb') as f:
        raw = pickle.load(f)
        setattr(module, 'test_results', raw)


def compare_sets(x, y, test_name):
    assert len(x) == len(
        y), f'Failure while testing {test_name}:\n Expected list of length {len(x)} but got {len(y)}'
    assert isinstance(x, type(
        y)), f'Failure while testing {test_name}:\n Expected type {type(x)} but got {type(y)}'
    
    assert x == y, f'Failure while testing {test_name}: Expected\n {x} \nbut got\n {y} \n missing: {y-x} \n extra: {x-y}'

def verify(inputs, expecteds, test_name, test_func):

    for i, inp in enumerate(inputs):
        try:
            res = test_func(*inp)
        except RecursionError:
            res = "RecursionError!"
        
        expected = expecteds[i]

        assert isinstance(res, type(expected)), f'Failure while testing {test_name}:\n Expected type {type(expected)} but got {type(res)}'
        if isinstance(expected, int):
            inp_message = "" if len(inp[0]) > 5 else f"\ninputs:\n{inp}"
            assert expected == res, f'Failure while testing {test_name}:\nExpected {expected} but got {res} {inp_message}'
        else:
            compare_sets(expected, res, test_name)

def test_count_subparts():
    test_name = 'count_subparts'
    inp = test_results[test_name]['tests']
    exp = test_results[test_name]['results']
    test_func = practice.count_subparts
    verify(inp, exp, test_name, test_func)

def test_maximum_steps():
    test_name = 'maximum_steps'
    inp = test_results[test_name]['tests']
    exp = test_results[test_name]['results']
    test_func = practice.maximum_steps
    verify(inp, exp, test_name, test_func)

def test_find_base_parts():
    test_name = 'find_base_parts'
    inp = test_results[test_name]['tests']
    exp = test_results[test_name]['results']
    test_func = practice.find_base_parts
    verify(inp, exp, test_name, test_func)


if __name__ == '__main__':
    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action='store_true')
    parser.add_argument("--server", action='store_true')
    parser.add_argument("--initial", action='store_true')
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()

    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {'passed': []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(
                report.outcome,
                []).append(
                report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]

    pytest_args = ['-v', __file__]

    if parsed.server:
        pytest_args.insert(0, '--color=yes')

    if parsed.gather:
        pytest_args.insert(0, '--collect-only')

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ['-k', ' or '.join(parsed.args), *pytest_args],
        **{'plugins': [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(os.path.join(_dir, 'alltests.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.alltests))
                f.write('\n')
        else:
            with open(os.path.join(_dir, 'results.json'), 'w' if parsed.initial else 'a') as f:
                f.write(json.dumps(testinfo.results))
                f.write('\n')
