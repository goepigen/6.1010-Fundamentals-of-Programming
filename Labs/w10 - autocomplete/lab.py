"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!

import string  # optional import

# import pprint # optional import
# import typing # optional import
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        if not isinstance(key, str):
            raise TypeError

        node = self

        for letter in key:
            next_node = node.children.get(letter, None)
            if next_node:
                node = next_node
            else:
                new_node = PrefixTree()
                node.children[letter] = new_node
                node = new_node
        node.value = value

    def _get_node(self, key):
        if not isinstance(key, str):
            raise TypeError

        node = self

        for letter in key:
            next_node = node.children.get(letter, None)
            if next_node:
                node = next_node
            else:
                raise KeyError(f"Key {key!r} not found in PrefixTree")
        return node

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        node = self._get_node(key)
        if node.value is None:
            raise KeyError(f"Key {key} has no value in PrefixTree")
        return node.value

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        try:
            node = self._get_node(key)
            return node.value is not None
        except KeyError:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """
        if self.value is not None:
            yield ("", self.value)

        for letter, child_node in self.children.items():
            for suffix, value in child_node:
                yield (letter + suffix, value)
            # yield from ((letter +  key, value) for key, value in child_node)

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        node = self._get_node(key)

        if node.value is None:
            raise KeyError(f"Key {key} has no value in PrefixTree")

        node.value = None


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    words = {}
    sentences = tokenize_sentences(text)
    for s in sentences:
        for w in s.split():
            words[w] = words.get(w, 0) + 1
    tree = PrefixTree()
    for w, freq in words.items():
        tree[w] = freq
    return tree


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    try:
        node = tree._get_node(prefix)
    except KeyError:
        return []

    completions = [(prefix + suffix, freq) for suffix, freq in node]

    completions.sort(key=lambda item_freq: item_freq[1], reverse=True)

    if max_count is not None:
        completions = completions[:max_count]

    return [word for word, _ in completions]


def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    completions = autocomplete(tree, prefix, max_count)
    seen = set(completions)

    if max_count is None:
        edits = [e for e in single_edits(tree, prefix) if e not in seen]
        edits.sort(key=lambda word: tree[word], reverse=True)
        return completions + edits

    missing = max_count - len(completions)
    if missing <= 0:
        return completions

    suggestions = completions.copy()

    edits = [edit for edit in single_edits(tree, prefix) if edit not in seen]
    edits.sort(key=lambda edit: tree[edit], reverse=True)
    return suggestions + edits[:missing]


def word_filter(tree, pattern):
    """
    Return set of (word, value) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    if pattern == "":
        return {("", tree.value)} if tree.value is not None else set()

    first = pattern[0]
    rest = pattern[1:]

    if first == "?":
        filtered = set()
        for letter, node in tree.children.items():
            child_filtered = word_filter(node, rest)
            filtered.update(
                {
                    (letter + child_pattern, freq)
                    for child_pattern, freq in child_filtered
                }
            )
        return filtered

    if first == "*":
        filtered = set()

        filtered.update(word_filter(tree, rest))

        for letter, node in tree.children.items():
            child_filtered = word_filter(node, pattern)
            filtered.update(
                {(letter + suffix, freq) for suffix, freq in child_filtered}
            )
        return filtered

    if first in tree.children:
        next_node = tree.children[first]
        filtered = word_filter(next_node, rest)
        return {(first + child_pattern, freq) for child_pattern, freq in filtered}

    return set()


# HELPERS


def single_edits(tree, prefix):
    seen = set()

    yield from single_insertion_edits(tree, prefix, seen)
    yield from single_deletion_edits(tree, prefix, seen)
    yield from single_replacement_edits(tree, prefix, seen)
    yield from single_transpose_edits(tree, prefix, seen)


def single_insertion_edits(tree, prefix, seen):
    letters = string.ascii_lowercase

    for pos in range(len(prefix) + 1):
        for letter in letters:
            edit = prefix[:pos] + letter + prefix[pos:]
            yield from yield_if_valid(tree, edit, seen)


def single_replacement_edits(tree, prefix, seen):
    letters = string.ascii_lowercase

    for pos in range(len(prefix)):
        for letter in letters:
            edit = prefix[:pos] + letter + prefix[pos + 1 :]
            yield from yield_if_valid(tree, edit, seen)


def single_deletion_edits(tree, prefix, seen):
    for pos in range(len(prefix)):
        edit = prefix[:pos] + prefix[pos + 1 :]
        yield from yield_if_valid(tree, edit, seen)


def single_transpose_edits(tree, prefix, seen):
    for pos in range(len(prefix) - 1):
        edit = prefix[:pos] + prefix[pos + 1] + prefix[pos] + prefix[pos + 2 :]
        yield from yield_if_valid(tree, edit, seen)


def yield_if_valid(tree, edit, seen):
    if edit in seen:
        return
    if edit in tree:
        seen.add(edit)
        yield edit


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # doctest.run_docstring_examples( # runs doctests for one function
    #    PrefixTree.__getitem__,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=True
    # )

    # end of assignment questions

    def read_file(name):
        with open(f"books/{name}.txt", encoding="utf-8") as f:
            return f.read()

    metamorphosis_text = read_file("metamorphosis")
    tale_text = read_file("a tale of two cities")
    alice_text = read_file("alice in wonderland")
    pride_text = read_file("pride and prejudice")
    dracula_text = read_file("dracula")

    metamorphosis_tree = word_frequencies(metamorphosis_text)
    tale_tree = word_frequencies(tale_text)
    alice_tree = word_frequencies(alice_text)
    pride_tree = word_frequencies(pride_text)
    dracula_tree = word_frequencies(dracula_text)

    result1 = autocomplete(metamorphosis_tree, "gre", 6)
    result2 = word_filter(metamorphosis_tree, "c*h")
    result3 = word_filter(tale_tree, "r?c*t")
    result4 = autocorrect(alice_tree, "hear", 12)
    result5 = autocorrect(pride_tree, "hear")
    result6 = len([el for el in dracula_tree])
    # result 6 = len(word_filter(dracula_tree, "*"))

    # This is tricky and not immediately useful to me so I did not spend time on it
    result7 = len(dracula_text.split())
    # result7 = len([w.strip(string.punctuation) for w in text.split() if w.strip(string.punctuation)])
