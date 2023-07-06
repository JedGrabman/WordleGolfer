#import os
#os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')

import pickle
from utilities import get_full_tree, tree_constructor, trim_tree, tree_dict_try_update

tree_set = set()
trees_to_analyze = set([get_full_tree()])
while trees_to_analyze:
    tree_working = trees_to_analyze.pop()
    if tree_working.subtree_small is not None:
        trees_to_analyze.add(tree_working.subtree_small)
        trees_to_analyze.add(tree_working.subtree_large)
    tree_set.add(tree_working)

tree_inversion_candidates = set()
for tree in tree_set:
    if tree.subtree_large is not None:
        if tree.subtree_large.subtree_large is not None:
            tree_split_pos = tree.tree_split_position
            if tree.subtree_large.tree_split_position == tree_split_pos:
                tree_inversion_candidates.add((tree, tree_split_pos, tree.subtree_large, ''.join(sorted(tree.letters[tree_split_pos])), ''.join(sorted(tree.tree_letter_group)), ''.join(sorted(tree.subtree_large.tree_letter_group))))
            if tree.subtree_small.tree_split_position == tree_split_pos:
                tree_inversion_candidates.add((tree, tree_split_pos, tree.subtree_small, ''.join(sorted(tree.letters[tree_split_pos])), ''.join(sorted(tree.tree_letter_group)), ''.join(sorted(tree.subtree_small.tree_letter_group))))

def make_tree_split(tree, letter_group, sub_letter_group, pos):
    start_bits_min = tree.bits_minimum
    trim_tree(tree)
    tree.create_subtree(letter_group, pos)
    if tree.subtree_small.letters[pos] == letter_group:
        subtree_split = tree.subtree_small
    else:
        subtree_split = tree.subtree_large
    subtree_split.create_subtree(sub_letter_group, pos)
    tree_dict_try_update(subtree_split.subtree_small)

    tree_constructor(subtree_split.subtree_small)
    tree_dict_try_update(subtree_split.subtree_large)
    tree_constructor(subtree_split.subtree_large)
    tree_dict_try_update(tree.subtree_small)
    tree_constructor(tree.subtree_small)
    tree_dict_try_update(tree.subtree_large)
    tree_constructor(tree.subtree_large)
    tree_dict_try_update(tree)
    tree_constructor(tree)
    end_bits_min = tree.bits_minimum
    assert end_bits_min <= start_bits_min, '{} is greater than {}'.format(end_bits_min, start_bits_min)
    
counter = 0
for combo in tree_inversion_candidates:
    counter += 1
    print('counter: {} / {}'.format(counter, len(tree_inversion_candidates)))
    tree = combo[0]
    start_bits_min = tree.bits_minimum
    tree_split_pos = combo[1]
    sub_group_1 = set(combo[3]).difference(set(combo[4]))
    sub_group_2 = set(combo[4])
    sub_group_3 = set(combo[5])
    if sub_group_1.intersection(sub_group_3):
        sub_group_1 = sub_group_1.difference(sub_group_3)
    else:
        sub_group_2 = sub_group_2.difference(sub_group_3)
    assert len(sub_group_1) + len(sub_group_2) + len(sub_group_3) == len(tree.letters[tree_split_pos])
    make_tree_split(tree, sub_group_1.union(sub_group_2), sub_group_1, tree_split_pos)
    make_tree_split(tree, sub_group_1.union(sub_group_2), sub_group_2, tree_split_pos)
    make_tree_split(tree, sub_group_1.union(sub_group_3), sub_group_1, tree_split_pos)
    make_tree_split(tree, sub_group_1.union(sub_group_3), sub_group_3, tree_split_pos)
    make_tree_split(tree, sub_group_2.union(sub_group_3), sub_group_2, tree_split_pos)
    make_tree_split(tree, sub_group_2.union(sub_group_3), sub_group_3, tree_split_pos)
    end_bits_min = tree.bits_minimum
    assert end_bits_min <= start_bits_min
