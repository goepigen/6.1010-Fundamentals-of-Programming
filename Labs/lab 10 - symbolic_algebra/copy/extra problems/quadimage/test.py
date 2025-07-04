"""
6.101 Optional Practice Exercises for Autocomplete:
QuadImage
"""

#!/usr/bin/env python3
import os
import pickle
import random
import pytest
import types 

import practice

TEST_DIRECTORY = os.path.dirname(__file__)

################### Testing helper methods
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

    with open(filename, 'rb') as f:
        raw = pickle.load(f)
        setattr(module, 'test_results_copy', raw)


def compare_sets(x, y, test_name):
    assert len(x) == len(
        y), f'Failure while testing {test_name}:\n Expected set of length {len(x)} but got {len(y)}'
    assert isinstance(x, type(
        y)), f'Failure while testing {test_name}:\n Expected type {type(x)} but got {type(y)}'
    for item in y:
        assert item in x, f'Failure while testing {test_name}:\n Item {item} not found in expected result'

# convert QuadImage into a nested dictionary... useful for visualizing the QuadImage
def dictify(q):
    expected_keys = {'width', 'height', 'pixel', 'quadrants'}
    assert set(q.__dict__) == expected_keys, f"Quadtree instances should only contain the instance attributes mentioned in the exercise. \n Extra vars: {set(q.__dict__) - expected_keys}"
    out = {k: q.__dict__[k] for k in expected_keys}
    out['quadrants'] = []
    for qc in q.quadrants:
        out['quadrants'].append(dictify(qc))
    return out
 
def _helper(im, image_dict, test_name, test_func):
    quad = practice.QuadImage(image_dict)  
    y = test_func(quad) 
    x = test_results[test_name][im]
    assert isinstance(y, types.GeneratorType), f'{test_name}  {im.split("/"[-1])}: \nExpected result to be generator but got {type(y)}'
    y = set(y)
    compare_sets(x, y, f'{test_name}  {im.split("/"[-1])}')

def _point_helper(im, image_dict, test_name, test_func):
    quad = practice.QuadImage(image_dict)
    for point in test_results[test_name][im]:
        expected_val = image_dict['pixels'][point[0]+point[1]*image_dict['width']]
        result = test_func(quad, point)
        assert result == expected_val, f'{test_name}  {im.split("/"[-1])} Expected arg {point} to get {expected_val} != Result {result}'

############        Test Cases:

def test_getitem_tiny():
    test_name = 'get'
    test_func = practice.QuadImage.__getitem__
    image_dict = {
        "width": 8,
        "height": 8,
        "pixels": [
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                ],
    }
    im_name = 'resources/tiny_sq.png'
    _point_helper(im_name, image_dict, test_name, test_func)
    
def test_getitem_square():
    test_name = 'get'
    test_func = practice.QuadImage.__getitem__
    im_names = [im for im in test_results['image_dict'] if 'sq' in im]
    for im in im_names:
        image_dict = test_results['image_dict'][im]
        _point_helper(im, image_dict, test_name, test_func)

def test_getitem_random():
    test_name = 'get'
    test_func = practice.QuadImage.__getitem__
    # pick random image:
    im_names = [im for im in test_results['image_dict'] if 'sq' not in im]
    random.shuffle(im_names)
    for im in im_names[:5]:
        image_dict = test_results['image_dict'][im]
        _point_helper(im, image_dict, test_name, test_func)

############

def test_iter_tiny():
    test_name = 'iter'
    test_func = practice.QuadImage.__iter__
    image_dict = {
        "width": 8,
        "height": 8,
        "pixels": [
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                    100, 100, 100, 100,  50,  50,  50,  50,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                      0,   0,   0,   0, 250, 250, 250, 250,
                ],
    }
    im = 'resources/tiny_sq.png'
    _helper(im, image_dict, test_name, test_func)
    
def test_iter_square():
    test_name = 'iter'
    test_func = practice.QuadImage.__iter__
    im_names = [im for im in test_results['image_dict'] if 'sq' not in im]
    for im in im_names:
        image_dict = test_results['image_dict'][im]
        _helper(im, image_dict, test_name, test_func)

def test_iter_random():
    test_name = 'iter'
    test_func = practice.QuadImage.__iter__
    im_names = [im for im in test_results['image_dict'] if 'sq' not in im]
    random.shuffle(im_names)
    for im in im_names:
        image_dict = test_results['image_dict'][im]
        _helper(im, image_dict, test_name, test_func)


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
