"""
6.101
SAT Optional Practice Exercises: Pigeons
"""

#!/usr/bin/env python3
import os
import pickle
import random
import pytest
import json

import practice

TEST_DIRECTORY = os.path.dirname(__file__)


def legal_assignment(birds, cities, result):
    # defend against ill-formed results
    assert type(result) == dict, f'Expected assign_cities to return a dictionary, got {type(result)}'
    assigned = set()
    pigeons = {p[0]: p[1] for p in birds} 
    # each destination must have a pigeon
    errmsg = f'#Given Input pigeons:\n{birds=}\n#Input destinations:{cities=}\n#Result from your code:\n{result=}'
    assert len(result) == len(cities), f'Expected length of result {len(result)} to equal number of destinations {len(cities)}' + errmsg

    found_cities = cities.copy()
    for pigeon, city in result.items():
        assert city in pigeons[pigeon], f'Pigeon {pigeon} assigned to {city}, which they cannot fly to!' + errmsg
        assert city in found_cities, f'Pigeon {pigeon} assigned to {city}, which is not expected!' + errmsg
        found_cities.remove(city)


def check_assign_cities(birds, cities, expect):
    birds2 =[(p[0], p[1].copy()) for p in birds]
    cities2 = [n for n in cities]
    result = practice.assign_cities(birds2, cities2)
    if expect:
        legal_assignment(birds, cities, result)
    else:
        assert result is None, f'Expected result to be None, but got {result}' 


def test_cities_01():
    # each pigeon in the pigeons list has a unique name
    # destination cities do not have to be unique
    # in each solution note how pigeons can only be assigned one destination
    simple_cases = [([('Milo', {'TRC'}), ('Sophie', {'TEY'}), ('Kotaro', {'LOM'})], # pigeons
                    ['LOM', 'TRC', 'TEY'], # destinations
                    {'Kotaro':'LOM', 'Milo': 'TRC', 'Sophie': 'TEY'}), # expected results
    ([('Lucy', {'FAS', 'WUH', 'ATZ'}), ('Sixten', {'FAS', 'WUH', 'ATZ'}), ('Sandy', {'FAS', 'WUH', 'ATZ'})], 
        ['ATZ', 'WUH', 'FAS'], 
        {'Sandy':'ATZ', 'Sixten':'WUH', 'Lucy': 'FAS'}), 
        # any mapping will work - all pigeons can reach all destinations
    ([('Oliver', {'NTR'}), ('Piper', {'NTR', 'AVU', 'DJU'}), ('Jasmine', {'NTR', 'DJU'})], 
        ['AVU', 'DJU', 'NTR'], 
        {'Piper': 'AVU', 'Jasmine': 'DJU', 'Oliver': 'NTR'}), 
    ([('Sandy', {'NDK', 'ESE'}), ('Nadine', {'NDK', 'ESE'}), ('Scout', {'NDK', 'ESE'})], 
        ['GPS', 'NDK', 'ESE'], 
        None), # no solution - no pigeon can fly to GPS
    ([('Kona', {'KNZ', 'ONE'}), ('Olive', {'KNZ', 'ONE', 'PVO'}), ('Lily', set())], 
        ['ONE', 'PVO', 'KNZ'], 
        None), 
    ([('Gus', {'PKX'}), ('Lightning', {'PKX', 'VAO'}), ('Thor', {'CSX', 'SAN'})], 
        ['VAO', 'PKX'], 
        {'Lightning': 'VAO', 'Gus': 'PKX'}), # note some pigeons may not be assigned
    ([('Bentley', {'TZM'}), ('Venus', {'AFT', 'BGJ'}), ('Hank', {'BLO', 'TZM'})], 
        ['TZM', 'TZM'], 
        # note some destinations may be repeated, but must be assigned to different pigeons
        {'Hank': 'TZM', 'Bentley': 'TZM'})]

    for i in range(len(simple_cases)):
        pigeons, destinations, expect = simple_cases[i]
        check_assign_cities(pigeons, destinations, expect)

def test_cities_02():
    cases = [([('Scout', {'XAL'}), ('Pelican', {'BIB'}), ('Pepper', {'MLM'})], 
                ['XAL', 'MLM', 'BIB'], ['Scout', 'Pepper', 'Pelican']), 
    ([('Jack', {'BOS', 'CLT', 'CTM'}), ('Winnie', {'BOS', 'CLT', 'CTM'}), ('Ollie', {'BOS', 'CLT', 'CTM'})], 
        ['CTM', 'BOS', 'CLT'], {'Winnie': 'CTM', 'Ollie': 'BOS', 'Jack': 'CLT'}), 
    ([('Apurva', {'HLO', 'LML'}), ('Coco', {'HLO', 'GEF', 'LML'}), ('Cora', {'LML'})], 
        ['GEF', 'HLO', 'LML'], {'Coco': 'GEF', 'Apurva': 'HLO', 'Cora': 'LML'}), 
    ([('Sigge', {'DEL', 'MCO'}), ('Duif', {'DEL', 'MCO'}), ('Athena', {'DEL', 'MCO'})], 
        ['DEL', 'PVO', 'MCO'], None), 
    ([('Katie', set()), ('Sigge', {'KDO', 'IXD', 'NIX'}), ('Jasper', {'KDO', 'IXD'})], 
        ['NIX', 'IXD', 'KDO'], None), 
    ([('Comet', {'MCO'}), ('Rosie', {'LAX', 'MBU'}), ('Teddy', {'CEN', 'MCO'})], 
        ['CEN', 'MCO'], {'Teddy': 'CEN', 'Comet': 'MCO'}), 
    ([('Sora', {'FCO', 'IAH'}), ('Hazel', {'KDO', 'KEF'}), ('Amardeep', {'FCO'})], 
        ['FCO', 'FCO'], {'Sora': 'FCO', 'Amardeep': 'FCO'})]
    for i in range(len(cases)):
        pigeons, destinations, expect = cases[i]
    check_assign_cities(pigeons, destinations, expect)

def test_lottery_1():
    prairie_dogs = [[2], [1], [0]]
    capacities = [1,1,1]
    result = practice.lottery(prairie_dogs,capacities)
    expected = [2,1, 0]
    assert result == expected, f"Lottery result {result} != expected {expected}"


def test_lottery_2():
    prairie_dogs = [[0, 1], [1, 0], [0, 1]]
    capacities = [1,1]
    result = practice.lottery(prairie_dogs,capacities)
    assert result == None,f"No solution, expected None for {prairie_dogs=}, {capacities=}"

def test_lottery_3():
    prairie_dogs = [[0, 1], [2, 3], [4, 5], [0], [2], [4]]
    capacities = [1,1,1,1,1,1]
    result = practice.lottery(prairie_dogs,capacities)
    expected = [1, 3, 5, 0, 2, 4]
    assert result == expected, f"Lottery result {result} != expected {expected}"

def test_lottery_4():
    with open(os.path.join(TEST_DIRECTORY,'resources','lottery_4.json'),'r') as f:
        expected = json.load(f)

    prairie_dogs = [[19, 18], [24, 7], [20, 25], [21, 1], [20, 24], [15, 14], [27, 13], [28, 15], [13, 20], [26, 11], [29, 17], [3, 20], [20, 28], [20, 27], [7, 20], [1, 0], [20, 29], [11, 20], [9, 8], [17, 20], [13, 12], [23, 5], [20, 22], [1, 20], [15, 20], [20, 26], [20, 21], [19, 20], [20, 30], [5, 4], [5, 20], [7, 6], [20, 23], [30, 19], [9, 20], [25, 9], [17, 16], [3, 2], [11, 10], [22, 3]]
    capacities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    result = practice.lottery(prairie_dogs,capacities)
    assert result in expected, f"Result {result} not one of expected results!"

def test_lottery_5():
    prairie_dogs = [[7], [2], [6, 0], [1, 0], [15, 0], [2, 0], [13], [13, 0], [8, 0], [5], [4], [3], [17, 0], [16], [11], [6], [7, 0], [10], [12, 0], [17], [11, 0], [20], [14, 0], [1], [20, 0], [18, 0], [19, 0], [15], [18], [4, 0], [10, 0], [19], [9], [5, 0], [9, 0], [14], [16, 0], [8], [12], [3, 0]]
    capacities = [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    result = practice.lottery(prairie_dogs,capacities)
    expected = [7, 2, 0, 0, 0, 0, 13, 0, 0, 5, 4, 3, 0, 16, 11, 6, 0, 10, 0, 17, 0, 20, 0, 1, 0, 0, 0, 15, 18, 0, 0, 19, 9, 0, 0, 14, 0, 8, 12, 0]
    assert result == expected,f"Lottery result {result} != expected {expected}"


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
            alltests = None
            results = {"passed": []}
            gather = gather

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != "call":
                return
            results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            if gather:
                alltests = [i.name for i in session.items]

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
