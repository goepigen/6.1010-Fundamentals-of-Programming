"""
6.101 Lisp 2 Optional Practice Exercises: Loopless
"""


#!/usr/bin/env python3
import os
import pickle
import random
import pytest

import practice

TEST_DIRECTORY = os.path.dirname(__file__)


def factorial(n):
    if n <= 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def length(x):
    if type(x) == str:
        return len(x)
    if x is None:
        return 0
    return 1 + length(x[1])


func_map = {
    "factorial": factorial,
    "lambda y: -y": lambda y: -y,
    "lambda y: y * 2 * y * 2": lambda y: y * 2 * y * 2,
    "lambda y: y**2": lambda y: y**2,
    "length": length,
    'lambda s: s[0] + "oom!"': lambda s: s[0] + "oom!",
    "lambda x: x%2 == 0": lambda x: x % 2 == 0,
    "lambda x: length(x) > 0": lambda x: length(x) > 0,
    "lambda x: x < 0": lambda x: x < 0,
    "lambda x: True": lambda x: True,
    "lambda x: False": lambda x: False,
    "lambda x: abs(x) > 2": lambda x: abs(x) > 2,
    "+": lambda val, x: val + x,
    "-": lambda val, x: val - x,
    "*": lambda val, x: val * x,
    "/": lambda val, x: val / x,
    "lambda val, x: val + length(x)": lambda val, x: val + length(x),
}


def setup_module(module):
    """
    This function loads the various databases.  It will be run once every time
    test.py is invoked.
    """
    filename = os.path.join(TEST_DIRECTORY, "resources", "tests.pickle")
    with open(filename, "rb") as f:
        raw = pickle.load(f)
        setattr(module, "test_results", raw)


def close_equal(exp, res):
    if type(exp) == float:
        return abs(exp - res) <= 1e-6
    return exp == res


def compare_results(inp, exp, res, test_name):
    err_msg = f"\n\tInput: {inp} \n\tExpected out: {exp}\n\tResult out: {res}"
    assert isinstance(
        res, type(exp)
    ), f"Failure while testing {test_name}:\n Expected type {type(exp)} but got {type(res)}. {err_msg}"

    if type(res) != tuple:
        assert close_equal(exp, res), f"Failure while testing {test_name}: {err_msg}"
    else:
        assert length(exp) == length(
            res
        ), f"Failure while testing {test_name}:\n Expected length {length(exp)} but got {length(res)}. {err_msg}"
        i = 0
        while exp != None:
            assert close_equal(
                exp[0], res[0]
            ), f"Failure while testing {test_name}: Element at index {i}: Expected\n {exp[0]} \nbut got\n {res[0]}. {err_msg}"
            i += 1
            exp = exp[1]
            res = res[1]


def test_map():
    test_name = "map"
    for inp, exp_out in test_results[test_name]:
        compare_results(inp, practice.map(inp[0], func_map[inp[1]]), exp_out, test_name)


def test_filter():
    test_name = "filter"
    for inp, exp_out in test_results[test_name]:
        compare_results(
            inp, practice.filter(inp[0], func_map[inp[1]]), exp_out, test_name
        )


def test_reduce():
    test_name = "reduce"
    for inp, exp_out in test_results[test_name]:
        compare_results(
            inp, practice.reduce(inp[0], func_map[inp[1]], inp[2]), exp_out, test_name
        )


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
