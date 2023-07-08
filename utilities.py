#import os
#os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')

import operator as op
from functools import reduce
from wordle_tree import wordle_tree

import pickle

TREE_DICT_FILE = 'tree_dict.txt'

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

def get_wordle_words():
    word_list = open('word_list.js')
    words = word_list.readlines()
    word_list.close()
    words = {word[0:5] for word in words}
    return words

def flatten_letters(letter_groups):
    return tuple(''.join(sorted(letter_group)) for letter_group in letter_groups)

def flatten_tree_letters(tree):
    return flatten_letters(tree.letters)

def get_tree_dict(tree_dict_file = TREE_DICT_FILE):
    file = open(tree_dict_file, 'rb')
    tree_dict = pickle.load(file)
    file.close()
    return tree_dict

def save_tree_dict_to_file(tree_dict, tree_dict_file = TREE_DICT_FILE):
    file = open(tree_dict_file, 'wb')
    pickle.dump(tree_dict, file)
    file.close()

def tree_constructor(tree, tree_dict = None, use_default_tree_dict = False, words = get_wordle_words()):
    # Forcing users to explicitly opt in to using saved tree_dict, since using
    # it unintentionally can cause severely misleading results
    if tree_dict is None and not use_default_tree_dict:
        raise ValueError('tree_dict required or set use_default_tree_dict to True!')
    elif use_default_tree_dict:
        tree_dict = get_tree_dict()
    tree_bits_min_start = tree.bits_minimum
    words_valid = {word for word in words if all(word[i] in tree.letters[i] for i in range(len(tree.letters)))}
    flat_letters = flatten_tree_letters(tree)
    if flat_letters in tree_dict:
        tree_split_position = tree_dict[flat_letters][1]
        if tree_split_position is None:
            if tree.parent:
                tree.parent.update_bits_minimum()
        else:
            tree_letter_group = set(tree_dict[flat_letters][2])
            tree.create_subtree(tree_letter_group, tree_split_position)
            if tree.subtree_small.bits_minimum > tree_dict[flatten_tree_letters(tree.subtree_small)][0]:
                tree_constructor(tree.subtree_small, tree_dict)
            if tree.subtree_large.bits_minimum > tree_dict[flatten_tree_letters(tree.subtree_large)][0]:
                tree_constructor(tree.subtree_large, tree_dict)
    else:
        raise ValueError('tree ({}) is not in tree_dict! try running tree_dict_try_update first!'.format(flatten_tree_letters(tree)))
    tree_bits_min_end = tree.bits_minimum
    assert tree_bits_min_end <= tree_bits_min_start, 'tree {} had its bits_minimum increase!'.format(flatten_tree_letters(tree))

def tree_dict_try_update(tree, tree_dict, reconstruct_trees = True):
    bits_min_start = tree.bits_minimum
    if not tree.leaf:
        tree_dict_try_update(tree.subtree_large, tree_dict)
        tree_dict_try_update(tree.subtree_small, tree_dict)

    if reconstruct_trees:
        if not tree.leaf:
            subtree_large_letters = flatten_tree_letters(tree)
            if subtree_large_letters not in tree_dict:
                tree_dict_insert_or_update(tree, tree_dict)
            if tree.subtree_large.bits_minimum > tree_dict[subtree_large_letters][0]:
                tree_constructor(tree.subtree_large)

            subtree_small_letters = flatten_tree_letters(tree)
            if subtree_small_letters not in tree_dict:
                tree_dict_insert_or_update(tree, tree_dict)
            if tree.subtree_small.bits_minimum > tree_dict[subtree_small_letters][0]:
                tree_constructor(tree.subtree_small)

    tree_dict_insert_or_update(tree, tree_dict)
    bits_min_end = tree.bits_minimum
    assert bits_min_end <= bits_min_start

def tree_dict_insert_or_update(tree, tree_dict):
    tree_letters = flatten_tree_letters(tree)
    tree_bits = tree.bits_minimum
    if tree.leaf:
        tree_letter_group = None
    else:
        tree_letter_group = ''.join(sorted(tree.tree_letter_group))
    tree_info = (tree_bits, tree.tree_split_position, tree_letter_group)
    if tree_letters in tree_dict:
        min_bits_seen = tree_dict[tree_letters][0]
        if tree_bits < min_bits_seen:
            tree_dict[tree_letters] = tree_info
    else:
        tree_dict[tree_letters] = tree_info

def get_full_tree():
    words = get_wordle_words()
    tree = wordle_tree([set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)], {word for word in words})
    tree_constructor(tree)
    return tree

def trim_tree(tree):
    tree.tree_letter_group = None
    tree.tree_split_position = None
    tree.subtree_small = None
    tree.subtree_large = None
    tree.bits_minimum = tree.find_bits()
    if tree.parent:
        tree.parent.update_bits_minimum()
    tree.set_done(False)

def tree_dict_update_and_save(tree, tree_dict, tree_dict_file = TREE_DICT_FILE):
    tree_dict_try_update(tree, tree_dict)
    save_tree_dict_to_file(tree_dict, tree_dict_file)

def tree_from_letters(letters, words = get_wordle_words()):
    letters = [set(letter_group) for letter_group in letters]
    valid_words = {word for word in words if all(word[i] in letters[i] for i in range(len(letters)))}
    tree = wordle_tree(letters, valid_words)
    return tree

# This is mostly useful if the wordle_tree algorithm has been updated
def rebuild_and_save_tree_dict():
    tree_dict = get_tree_dict()
    for letter_group in tree_dict.keys():
        tree = tree_from_letters(letter_group)
        tree_dict_try_update(tree, tree_dict)
    save_tree_dict_to_file(tree_dict)

def get_tree_set(tree):
    tree_set = set()
    trees_to_analyze = set([tree])
    while trees_to_analyze:
        tree = trees_to_analyze.pop()
        if not tree.leaf:
            trees_to_analyze.add(tree.subtree_small)
            trees_to_analyze.add(tree.subtree_large)
        tree_set.add(tree)
    return tree_set