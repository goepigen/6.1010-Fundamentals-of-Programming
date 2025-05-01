"""
6.101 Lab:
SAT Solver
"""

#!/usr/bin/env python3

# import typing  # optional import
# import pprint  # optional import
import doctest
import sys

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

# HELPERS


def update_formula(formula, assignments):
    """
    Given a formula in CNF form and assignments of variables to Boolean values,
    update the formula by, for each variable assignment, visiting each clause in
    the conjunctive formula, traversing each clause variable by variable, comparing
    the truth value of the variable in the formula with the variable assignment,
    removing the clause from the formula if the truth values match (because it is a
    True variable in a disjunction, making the disjunctive clause True), or removing
    the variable from the disjunctive clause if the truth values don't match (because
    it is a False variable in a disjunction, so it doesn't affect the truth value of
    the rest of the disjunctive clause).
    After visiting any clause in this process, if the resulting clause is an empty list, it
    is because all the variables in the disjunctive clause are False, and so the entire formula
    (a conjunction) must be false, so None is returned (the formula is false).
    After considering all the variables that are assigned to a Boolean, the updated formula is
    returned. Note that if this updated formula is empty, it means all the clauses in the input
    formula are True, so the updated formula is always True.
    Args:
        formula: list of lists, representing a Boolean expression in CNF
        assignments: dict of variable: Boolean pairs
    Returns:
        None if formula with variables assigned as in assignments leads to a new formula
        that is always False.
        New formula in CNF otherwise.
        An empty list means that the new formula is always True, ie the assignments make the
        formula True.
    """
    current_formula = formula

    for assigned_var, val in assignments.items():
        new_formula = []
        for clause in current_formula:
            new_clause = []
            satisfied = False
            for var in clause:
                if var[0] == assigned_var:
                    if var[1] == val:
                        # go to next clause (remove from formula (conjunctive) because always True)
                        satisfied = True
                        break
                    # if var[1] != val then do nothing (ie, remove from disjunctive clause because always False)
                else:
                    new_clause.append(var)
            # if there are no variables in a disjunction, the latter is False, so the
            # conjunctive formula is False
            if satisfied:
                continue
            if not new_clause:
                return None
            new_formula.append(new_clause)
        current_formula = new_formula

    return current_formula


def satisfied_formula(formula):
    return len(formula) == 0


def remove_length_one_clauses(formula):
    updated_formula = formula

    forced_assignments = {}

    if updated_formula is None:
        return None

    length_one_clauses = [el for el in updated_formula if len(el) == 1]

    while length_one_clauses:
        assignments = {clause[0][0]: clause[0][1] for clause in length_one_clauses}
        forced_assignments.update(assignments)
        updated_formula = update_formula(updated_formula, assignments)
        if updated_formula is None:
            return None, None
        length_one_clauses = [el for el in updated_formula if len(el) == 1]

    return updated_formula, forced_assignments


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> T, F = True, False
    >>> x = satisfying_assignment([[('a', T), ('b', F), ('c', T)]])
    >>> x.get('a', None) is T or x.get('b', None) is F or x.get('c', None) is T
    True
    >>> satisfying_assignment([[('a', T)], [('a', F)]])
    """

    updated_formula, forced_assignments = remove_length_one_clauses(formula)

    if updated_formula is None:
        return None

    if satisfied_formula(updated_formula):
        return forced_assignments

    first_clause = updated_formula[0]
    fc_vars = [el[0] for el in first_clause]

    for v in fc_vars:
        for truth_value in [True, False]:
            assignments = {v: truth_value}
            # try to find solution with v assigned
            new_formula = update_formula(updated_formula, assignments)
            if new_formula is None:
                continue
            if satisfied_formula(new_formula):
                return {**forced_assignments, **assignments}
            result = satisfying_assignment(new_formula)
            if result is not None:
                return {**forced_assignments, **assignments, **result}
    return None


def only_desired_rooms(student_preferences, room_capacities):
    rooms = room_capacities.keys()
    students = student_preferences.keys()
    student_non_preferences = {
        s: {r for r in rooms if r not in student_preferences[s]} for s in students
    }
    return [
        [(f"{s}_{r}", False)] for s, rs in student_non_preferences.items() for r in rs
    ]


def combinations(lst, k):
    if k == 0:
        yield []
    elif len(lst) < k:
        return
    else:
        first, rest = lst[0], lst[1:]
        for c in combinations(rest, k - 1):
            yield [first] + c
        yield from combinations(rest, k)


def one_session_per_student(student_preferences, room_capacities):
    rooms = list(room_capacities)
    students = list(student_preferences)
    room_pairs = list(combinations(rooms, 2))

    return [
        [(f"{s}_{r[0]}", False), (f"{s}_{r[1]}", False)]
        for s in students
        for r in room_pairs
    ] + [[(f"{s}_{r}", True) for r in rooms] for s in students]


def no_oversubscribed_rooms(student_preferences, room_capacities):
    students = list(student_preferences)
    n_students = len(students)
    rooms = [r for r, cap in room_capacities.items() if cap < n_students]

    return [
        [(f"{s}_{r}", False) for s in student_combinations]
        for r in rooms
        for student_combinations in combinations(students, room_capacities[r] + 1)
    ]


def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    cnf = [
        *only_desired_rooms(student_preferences, room_capacities),
        *one_session_per_student(student_preferences, room_capacities),
        *no_oversubscribed_rooms(student_preferences, room_capacities),
    ]

    return cnf


if __name__ == "__main__":
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)
    student_preferences = {
        "alex": {"basement", "penthouse"},
        "blake": {"kitchen"},
        "chris": {"basement", "kitchen"},
        "dana": {"kitchen", "penthouse", "basement"},
    }

    room_capacities = {"basement": 1, "kitchen": 2, "penthouse": 4}
    rooms = list(room_capacities)
    rooms1 = get_pairs_from_list(rooms)
    rooms2 = combinations(rooms, 2)

    one_session_per_student(student_preferences, room_capacities)

    # formula = boolify_scheduling_problem(student_preferences, room_capacities)

    # result = satisfying_assignment(formula)
