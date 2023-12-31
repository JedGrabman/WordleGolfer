#import os
#os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')

from wordle_tree import wordle_tree
import math
import operator as op
from functools import reduce
import pickle
from utilities import ncr, get_wordle_words

#encoder
def encode_choice(input_list):
    value = 0
    num = 0
    denom = 1
    total = 0
    for i in range(len(input_list)):
        while num < input_list[i]:
            if num < denom - 1:
                value = 0
            if num == denom - 1:
                value = 1
            else:
                value = value * (num + 1) // (num + 1 - denom)
            num = num + 1
        total = total + value
        if num == denom:
            value = 0
        else:
            value = (value * (num - denom)) // (denom + 1)
        denom = denom + 1
    return(total)

def encode_words(letter_sets, words):
    letter_groups = [sorted(letter_set) for letter_set in letter_sets]
    base_per_position = [len(letter_group) for letter_group in letter_groups]
    place_per_position = [1] * len(base_per_position)
    for i in reversed(range(len(base_per_position) - 1)):
        place_per_position[i] = base_per_position[i + 1] * place_per_position[i + 1]

    word_nums = words_to_indexes(letter_groups, words, place_per_position)
    word_nums = sorted(word_nums)
    encoding = encode_choice(word_nums)
    possibilities = place_per_position[0] * base_per_position[0]
    combo_num = ncr(possibilities, len(words))
    return (combo_num, encoding)

def words_to_indexes(letter_groups, words, place_per_position):
    result_array = []
    for word in words:
        word_sum = 0
        for i in range(len(word)):
            letter = word[i]
            letter_index = [j for j in range(len(letter_groups[i])) if letter_groups[i][j] == letter][0]
            word_sum = word_sum + letter_index * place_per_position[i]
        result_array.append(word_sum)
    return(result_array)

#(subtree_large)(subtree_small)(words in subtree_small)(letter_flags)(split_position)
#1(words_encoding)(leaf flag)
# Note that the number of bits in the tree encoding may be slightly smaller than the tree.bits_minimum
# This appears to be because when the value of code is very small, the impact of adding a small vs. large 
# code_words value can meaningfully change log(code + code_words). For testing purposes, this effect can be
# eliminated by setting a large code value and subtracting off its impact on the log of the result
# e.g. (tree_encoder(tree, code = 2**10) - 10) is robust
def tree_encoder(tree, code = 0):
    if tree.subtree_large is None:
        words_encoding = encode_words(tree.letters, tree.words_valid)
        combos = words_encoding[0]
        code_words = words_encoding[1]
        code = code * combos + code_words
        code = code << 1 | 1

    else:
        code = tree_encoder(tree.subtree_large, code)
        code = tree_encoder(tree.subtree_small, code)
        code = code * (len(tree.words_valid) + 1)
        code = code + len(tree.subtree_small.words_valid)

        letter_flags = [letter in tree.tree_letter_group for letter in sorted(tree.letters[tree.tree_split_position])][::-1]
        for flag in letter_flags:
            code = code << 1
            if flag:
                code = code + 1
        code = code * 5 + tree.tree_split_position
        code = code << 1
    return code


def encode_123(input):
    # all 7 bit characters except null, new line, return, apostrophe and backslash
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    results = ''
    while(input > 0):
        remainder = input % 123
        results = results + foo[remainder]
        input = input // 123
    return(results)

letters_array = [set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)]
words_set = get_wordle_words()
tree = wordle_tree(letters_array, words_set)
tree.create_subtree(set('aeiou'), 0)
tree.subtree_large.create_subtree(set('aeiou'), 1)
tree.subtree_large.subtree_large.create_subtree(set('aeiou'), 2)
tree.subtree_large.subtree_large.subtree_large.create_subtree(set('aeiou'), 3)
tree.subtree_large.subtree_small.create_subtree(set('aeiou'), 2)
tree.subtree_large.subtree_small.subtree_large.create_subtree(set('aeiou'), 3)
tree.subtree_large.subtree_small.subtree_small.create_subtree(set('aeiou'), 3)

tree.subtree_small.create_subtree(set('aeiou'), 1)
tree.subtree_small.subtree_large.create_subtree(set('aeiou'), 2)
tree.subtree_small.subtree_large.subtree_large.create_subtree(set('aeiou'), 3)
tree.subtree_small.subtree_large.subtree_small.create_subtree(set('aeiou'), 3)

while not tree.done:
    tree.add_tree(True) # non-deterministic

tree_code = tree_encoder(tree)
tree_code_123 = encode_123(tree_code)

print(math.ceil(math.log(tree_code, 2))) # 81181 for utilities.get_full_tree()
print(math.ceil(math.log(tree_code, 123))) # 11694
print(tree_code_123)
#Note that '\x1b[' does not render when printing (at least in visual studio).
# you can however split on it:
#for x in(tree_code_123.split('\x1b[')): print(x)
# '\x1b[' == '['