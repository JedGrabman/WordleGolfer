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

def tree_constructor(tree, tree_dict = get_tree_dict(), words = get_wordle_words()):
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
            if tree.bits_minimum > tree_dict[flatten_tree_letters(tree)][0]:
                tree_constructor(tree.subtree_small)
                tree_constructor(tree.subtree_large)

def tree_dict_try_update(tree, tree_dict = get_tree_dict()):
    if tree.subtree_large:
        tree.update_bits_minimum()
    bits_min_start = tree.bits_minimum
    print('tree_dict_try_update: bits_min_start = {}'.format(bits_min_start))

    if tree.subtree_large:
        subtree_large_letters = flatten_tree_letters(tree)
        if tree.subtree_large.bits_minimum > tree_dict[subtree_large_letters][0]:
            tree_constructor(tree.subtree_large)
        subtree_small_letters = flatten_tree_letters(tree)
        if tree.subtree_small.bits_minimum > tree_dict[subtree_small_letters][0]:
            tree_constructor(tree.subtree_small)

    tree_letters = flatten_tree_letters(tree)
    tree_bits = tree.bits_minimum
    if tree.tree_letter_group:
        tree_letter_group = ''.join(sorted(tree.tree_letter_group))
    else:
        tree_letter_group = None
    tree_info = (tree_bits, tree.tree_split_position, tree_letter_group)
    if tree_letters in tree_dict:
        min_bits_seen = tree_dict[tree_letters][0]
        print('min_bits_seen: {}'.format(min_bits_seen))
        if tree_bits < min_bits_seen:
            tree_dict[tree_letters] = tree_info
            print('tree updated')
            print('checking subtrees:')
            if tree.subtree_large:
                tree_dict_try_update(tree.subtree_large)
                tree_dict_try_update(tree.subtree_small)
            print('checking parent:')
            if tree.parent:
                tree_dict_try_update(tree.parent)
    else:
        tree_dict[tree_letters] = tree_info
    bits_min_end = tree.bits_minimum
    assert bits_min_end <= bits_min_start

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
    if tree.parent:
        tree.parent.update_bits_minimum()
    tree.done = False