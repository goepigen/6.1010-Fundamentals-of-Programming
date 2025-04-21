"""
6.101 Lab:
Recipes
"""

import pickle
import sys

# import typing # optional import
# import pprint # optional import

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def atomic_ingredient_costs(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary mapping each atomic food name to its cost.
    """
    return {ing[1]: ing[2] for ing in recipes_db if ing[0] == "atomic"}


def compound_ingredient_possibilities(recipes_db):
    """
    Given a recipes database, a list containing compound and atomic food tuples,
    make and return a dictionary that maps each compound food name to a
    list of all the ingredient lists associated with that name.
    """
    ing_by_compound = {}

    for ing_entry in recipes_db:
        if ing_entry[0] == "atomic":
            continue

        ing_by_compound.setdefault(ing_entry[1], []).append(ing_entry[2])

    return ing_by_compound


def lowest_cost(recipes_db, food_name, forbidden_ings=()):
    """
    Given a recipes database and the name of a food (str), return the lowest
    cost of a full recipe for the given food item or None if there is no way
    to make the food_item.
    """
    if food_name in forbidden_ings:
        return None

    cost_by_atomic_ing = atomic_ingredient_costs(recipes_db)
    ing_lists_by_compound = compound_ingredient_possibilities(recipes_db)

    def lowest_cost_rec(food_name):
        if food_name in forbidden_ings:
            return None

        cost_if_atomic = cost_by_atomic_ing.get(food_name, None)

        # base case
        if cost_if_atomic is not None:
            return cost_if_atomic

        # recursive case
        ing_lists = ing_lists_by_compound.get(food_name, None)

        if not ing_lists:
            return None

        costs = []

        for ing_list in ing_lists:
            cost = 0
            for ing_entry in ing_list:
                ing_name = ing_entry[0]
                ing_unit_cost = lowest_cost_rec(ing_name)

                if ing_unit_cost is None:
                    cost = None
                    break

                quantity = ing_entry[1]
                cost += quantity * ing_unit_cost
            if cost is not None:
                costs.append(cost)

        return min(costs) if costs else None

    return lowest_cost_rec(food_name)


def scaled_recipe(recipe_dict, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    return {k: n * v for k, v in recipe_dict.items()}


def add_recipes(recipe_dicts):
    """
    Given a list of recipe dictionaries that map food items to quantities,
    return a new dictionary that maps each ingredient name
    to the sum of its quantities across the given recipe dictionaries.

    For example,
        add_recipes([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    keys = set().union(*recipe_dicts)

    merged_dict = {}

    for k in keys:
        merged_dict[k] = sum(rd.get(k, 0) for rd in recipe_dicts)

    return merged_dict


def cheapest_flat_recipe(recipes_db, food_name, forbidden_ings=(), debug=False):
    """
    Given a recipes database and the name of a food (str), return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    if food_name in forbidden_ings:
        return None

    cost_by_atomic_ing = atomic_ingredient_costs(recipes_db)
    ing_lists_by_compound = compound_ingredient_possibilities(recipes_db)

    def recipe_cost(r):
        return sum(v * cost_by_atomic_ing[k] for k, v in r.items())

    def cheapest_flat_recipe_rec(food_name, depth=0):
        indent = "  " * depth
        if debug:
            print(f"{indent}🔍 Checking: {food_name}")
        if food_name in forbidden_ings:
            if debug:
                print(f"{indent}🚫 Forbidden: {food_name}")
            return None

        if food_name in cost_by_atomic_ing:
            if debug:
                print(f"{indent}✅ Atomic: {food_name}")
            return {food_name: 1}

        if food_name not in ing_lists_by_compound:
            if debug:
                print(f"{indent}❓ No recipe: {food_name}")
            return None

        ing_lists = ing_lists_by_compound[food_name]

        recipes = []

        for ing_list in ing_lists:
            ing_recipes = []
            missing_ingredient = False
            for ing_entry in ing_list:
                ing_name = ing_entry[0]
                ing_recipe = cheapest_flat_recipe_rec(ing_name, depth + 1)
                if ing_recipe is None:
                    missing_ingredient = True
                    break

                quantity = ing_entry[1]
                ing_recipes.append(scaled_recipe(ing_recipe, quantity))

            if not missing_ingredient and ing_recipes:
                recipes.append(add_recipes(ing_recipes))

        # costs = [recipe_cost(r) for r in recipes]
        # min_index = costs.index(min(costs)) if costs else None
        # return recipes[min_index] if min_index is not None else None

        cheapest = min(recipes, key=recipe_cost, default=None)
        return cheapest

    return cheapest_flat_recipe_rec(food_name)


def combine_recipes(nested_recipes):
    """
    Given a list of lists of recipe dictionaries, where each inner list
    represents all the recipes for a certain ingredient, compute and return a
    list of recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    if len(nested_recipes) == 1:
        return nested_recipes[0]

    combined = combine_recipes(nested_recipes[1:])

    return [add_recipes([r, c]) for r in nested_recipes[0] for c in combined]


def all_flat_recipes(recipes_db, food_name, forbidden_ings=()):
    """
    Given a recipes database, the name of a food (str), produce a list (in any
    order) of all possible flat recipe dictionaries for that category.

    Returns an empty list if there are no possible recipes
    """
    if food_name in forbidden_ings:
        return []

    cost_by_atomic_ing = atomic_ingredient_costs(recipes_db)
    ing_lists_by_compound = compound_ingredient_possibilities(recipes_db)

    def all_flat_recipes_rec(food_name):
        if food_name in forbidden_ings:
            return []

        if food_name in cost_by_atomic_ing:
            return [{food_name: 1}]

        if food_name not in ing_lists_by_compound:
            return []

        ing_lists = ing_lists_by_compound[food_name]

        recipes = []

        for ing_list in ing_lists:
            ing_recipes = []
            missing_ingredient = False
            for ing_entry in ing_list:
                ing_name = ing_entry[0]
                ing_recipe = all_flat_recipes_rec(ing_name)
                if ing_recipe is None:
                    missing_ingredient = True
                    break

                quantity = ing_entry[1]
                ing_recipes.append([scaled_recipe(r, quantity) for r in ing_recipe])

            if not missing_ingredient and ing_recipes:
                recipes.extend(combine_recipes(ing_recipes))

        return recipes

    return all_flat_recipes_rec(food_name)


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes_db = pickle.load(f)
    with open("test_recipes/examples_filter.pickle", "rb") as f:
        test_data = pickle.load(f)

    result = cheapest_flat_recipe(example_recipes_db, "burger", ("tomato",), True)

    # for target, filt in test_data:
    # target = "salt"
    # filt = ("salt",)
    # graph = test._filter_graph(example_recipes_db, filt)
    # result = all_flat_recipes(example_recipes_db, target, filt)
    # expected = test_data[(target, filt)][0]
