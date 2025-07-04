"""
6.101 Lisp 1 Optional Practice Exercises: Boolean
"""


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
    filename = os.path.join(TEST_DIRECTORY, "resources", "tests.pickle")
    with open(filename, "rb") as f:
        raw = pickle.load(f)
        setattr(module, "test_results", raw)


def compare_results(inp, x, y, test_name):
    err_msg = f'\n\tInput: {inp} \n\tExpected out: {y}\n\tResult out: {x}'
    assert isinstance(
        x, type(y)
    ), f"Failure while testing {test_name}:\n Expected type {type(x)} but got {type(y)}. {err_msg}"

    if type(y) != list: 
        assert (
            x == y
        ), f"Failure while testing {test_name}: {err_msg}"
    else:
        
        assert len(x) == len(
            y
        ), f"Failure while testing {test_name}:\n Expected list of length {len(x)} but got {len(y)}. {err_msg}"

        for i, (sub_x, sub_y) in enumerate(zip(x, y)):
            assert (
                sub_x == sub_y
            ), f"Failure while testing {test_name}: Element at index {i}: Expected\n {sub_x} \nbut got\n {sub_y}. {err_msg}"


def test_expand():
    assert practice.expand("a") =='a'
    assert practice.expand("b6a") == 'baaaaaa'
    assert practice.expand("a2bc3d") == 'abbcddd'


def test_expand2():
    assert practice.expand("2{hi}") == 'hihi'
    assert len(practice.expand("30{2ops}")) == 120
    assert practice.expand("30{2ops}") == 'oops' * 30
    assert practice.expand("3{cat}dog") == 'catcatcatdog'
    assert practice.expand("3{2{2ac}d}4e") == 'aacaacdaacaacdaacaacdeeee'


def test_tokenize():
    test_name = 'tokenize_bool'
    for inp, exp_out in test_results[test_name]:
        compare_results(inp, practice.tokenize_bool(inp), exp_out, test_name)


def test_parse():
    test_name = 'parse_bool'
    for inp, exp_out in test_results[test_name]:
        compare_results(inp, practice.parse_bool(inp), exp_out, test_name)


if __name__ == "__main__":
    import sys
    import json
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gather", action="store_true")
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--initial", action="store_true")
    parser.add_argument("args", nargs="*")

    parsed = parser.parse_args()

    class TestData:
        def __init__(self, gather=False):
            self.alltests = None
            self.results = {"passed": []}
            self.gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != "call":
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if self.gather:
                self.alltests = [i.name for i in session.items]

    pytest_args = ["-v", __file__]

    if parsed.server:
        pytest_args.insert(0, "--color=yes")

    if parsed.gather:
        pytest_args.insert(0, "--collect-only")

    testinfo = TestData(parsed.gather)
    res = pytest.main(
        ["-k", " or ".join(parsed.args), *pytest_args], **{"plugins": [testinfo]}
    )

    if parsed.server:
        _dir = os.path.dirname(__file__)
        if parsed.gather:
            with open(
                os.path.join(_dir, "alltests.json"), "w" if parsed.initial else "a"
            ) as f:
                f.write(json.dumps(testinfo.alltests))
                f.write("\n")
        else:
            with open(
                os.path.join(_dir, "results.json"), "w" if parsed.initial else "a"
            ) as f:
                f.write(json.dumps(testinfo.results))
                f.write("\n")
