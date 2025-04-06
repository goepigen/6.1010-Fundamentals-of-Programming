# 6.101 recitation: lab 9 wrapup

from solution import PrefixTree, word_frequencies, autocomplete, autocorrect, word_filter

############################################ iterating

# class PrefixTree(PrefixTree):
#     def __iter__(self):
#         """
#         Generator of (key, value) pairs for all keys/values in this prefix tree
#         and its children.  Must be a generator!
#         """
#         pass    


# t = PrefixTree()
# t['bard'] = 8
# t['barbell'] = 9
# t['bar'] = 7

# print([(k,v) for k,v in t])





############################################ autocorrect

# def autocorrect(tree, prefix, max_count=None):
#     """
#     Return the list of the most-frequent words that start with prefix or that
#     are valid words that differ from prefix by a small edit.  Include up to
#     max_count elements from the autocompletion.  If autocompletion produces
#     fewer than max_count elements, include the most-frequently-occurring valid
#     edits of the given word as well, up to max_count total elements.
#     """
#     autocompletions = autocomplete(tree, prefix, max_count)
#     ...


# class PrefixTree(PrefixTree):

#     def autocorrect(self, key):
#         """
#         Generates (key,value) pairs for all valid keys in this tree that are 
#         exactly 1 edit away from `key`.
#         """
#         pass

# t = PrefixTree()
# t['cart'] = 1  # 'cat' with insert
# t['cats'] = 1  # 'cat' with insert
# t['at'] = 1    # 'cat' with delete
# t['cot'] = 1   # 'cat' with replace
# t['act'] = 1   # 'cat' with transpose
# t['cattle'] = t['crate'] = t['actor'] = t['a'] = 1  # too many edits
# print(list(t.autocorrect('cat')))