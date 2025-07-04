"""
6.101 Mines Optional Practice Exercises: Nesting
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


def compare_lists(x, y, test_name):
    assert len(x) == len(
        y
    ), f"Failure while testing {test_name}:\n Expected list of length {len(x)} but got {len(y)}"
    assert isinstance(
        x, type(y)
    ), f"Failure while testing {test_name}:\n Expected type {type(x)} but got {type(y)}"
    for i, (sub_x, sub_y) in enumerate(zip(x, y)):
        assert (
            sub_x == sub_y
        ), f"Failure while testing {test_name}: Element at index {i}: Expected\n {sub_x} \nbut got\n {sub_y}"


def test_pascal():
    levels = [i for i in range(1, 5)] + [
        random.randint(5, 15),
        random.randint(15, 25),
        random.randint(25, 100),
    ]
    expected = test_results["pascal"]
    for level in levels:
        exp = expected[:level] if level > 0 else []
        compare_lists(exp, practice.pascal(level), f"pascal({level})")


def test_fill_n_cube():
    inp = test_results["fnc"]["tests"]
    exp = test_results["fnc"]["results"]

    for i in range(len(inp)):
        ip, ep = inp[i], exp[i]
        compare_lists(ep, practice.fill_n_cube(ip), f"fill_n_cube({ip})")


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
