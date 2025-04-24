# 6.101 recitation: grammars

# goal: generate phrases based on patterns specified as a grammar

# a LITERAL is a word that should be produced verbatim in the output

# a RULE is a special kind of word that should not be produced verbatim in the
# output.  rather, each RULE has multiple ways of being instantiated, each of
# which consists of one or more words (each of which can itself be either a
# RULE or a LITERAL).

# a GRAMMAR is a mapping from RULEs to lists of ways that that rule can be
# satisfied.  any word not specifically specified in the grammar is a LITERAL


test_grammar_1 = {
    "sentence": [["noun", "verb"], ["noun", "never", "verb"]],
    "noun": [["pigs"], ["professors"]],
    "verb": [["fly"], ["think"]],
}

test_grammar_2 = {
    "start": [["n"], ["adj", "n"], ["adj", "adj", "n"]],
    "adj": [["quirky"], ["hungry"], ["n"]],
    "n": [["cat"], ["dog"]],
}

test_grammar_3 = {
    "greeting": [["hi", "there"], ["hi", "name"]],
    "name": [["Cameron"], ["someone"], ["Dana"], ["Bob", "Ross"]],
    "someone": [["you"]],
}


def one_phrase(grammar, root):
    """
    Using production rules from the grammar, expand the given root into any
    single valid phrase: a space-separated string containing only literal
    values.  If there are multiple valid phrases, any one is fine.
    """
    pass


def all_phrases(grammar, root):
    """
    Using production rules from the given grammar, return a set of all legal
    expansions of the given root, where each phrase is a space-separated string
    as above (i.e., each phrase is one option for what one_phrase could have
    returned).
    """
    pass














################
# TESTING CODE #
################


def _verify_all_phrases_result(L):
    # top level is a list
    if not isinstance(L, set):
        return False
    # each phrase is a list of strings
    for phrase in L:
        if not isinstance(phrase, tuple):
            return False
        for terminal in phrase:
            if not isinstance(terminal, str):
                return False
    return True

def test_all_phrases_1():
    assert all_phrases(test_grammar_1, "pigs") == {"pigs"}


def test_all_phrases_2():
    expected = {"pigs", "professors"}
    assert (
        all_phrases(
            test_grammar_1,
            "noun",
        )
        == expected
    )


def test_all_phrases_3():
    result = all_phrases(test_grammar_1, "sentence")
    expected = {
        "pigs fly",
        "pigs think",
        "professors fly",
        "professors think",
        "pigs never fly",
        "pigs never think",
        "professors never fly",
        "professors never think",
    }
    assert result == expected


def test_all_phrases_4():
    expected = {"hungry", "quirky", "cat", "dog"}
    assert all_phrases(test_grammar_2, "adj") == expected


def test_all_phrases_5():
    result = all_phrases(test_grammar_2, "start")
    expected = {
        "cat",
        "dog",
        "hungry cat",
        "hungry dog",
        "quirky cat",
        "quirky dog",
        "cat cat",
        "cat dog",
        "dog cat",
        "dog dog",
        "hungry hungry cat",
        "hungry hungry dog",
        "hungry quirky cat",
        "hungry quirky dog",
        "hungry cat cat",
        "hungry cat dog",
        "hungry dog cat",
        "hungry dog dog",
        "quirky hungry cat",
        "quirky hungry dog",
        "quirky quirky cat",
        "quirky quirky dog",
        "quirky cat cat",
        "quirky cat dog",
        "quirky dog cat",
        "quirky dog dog",
        "cat hungry cat",
        "cat hungry dog",
        "cat quirky cat",
        "cat quirky dog",
        "cat cat cat",
        "cat cat dog",
        "cat dog cat",
        "cat dog dog",
        "dog hungry cat",
        "dog hungry dog",
        "dog quirky cat",
        "dog quirky dog",
        "dog cat cat",
        "dog cat dog",
        "dog dog cat",
        "dog dog dog",
    }
    assert result == expected


def test_all_phrases_6():
    result = all_phrases(test_grammar_3, "greeting")
    expected = {
        "hi there",
        "hi Cameron",
        "hi Dana",
        "hi Bob Ross",
        "hi you",
    }
    assert result == expected


if __name__ == "__main__":
   testfuncs = {
       k: v for k, v in globals().items() if k.startswith("test_") and callable(v)
   }
   for name, func in testfuncs.items():
       print("running", name)
       func()
