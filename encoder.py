import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')

from wordle_tree import wordle_tree
import math
import operator as op
from functools import reduce
import pickle

word_list = open('word_list.js')
words = word_list.readlines()
word_list.close()
words = [word[0:5] for word in words]

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

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
    num_bits = math.ceil(math.log(combo_num, 2))
    return (num_bits, encoding)

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

def indexes_to_words(word_indexes, letter_groups, place_per_position):
    result_words = []
    for i in range(len(word_indexes)):
        word_num = word_indexes[i]
        start_word_num = word_num

        word = ''
        for j in range(len(letter_groups)):
            letter_index = word_num // place_per_position[j]
            word = word + letter_groups[j][letter_index]
            word_num = word_num % place_per_position[j]
        result_words.append(word)
    return(result_words)

#(subtree_large)([-1]subtree_small)(words in subtree_small)(letter_flags)(split_position)
#1(words_encoding)(111)
def tree_encoder(tree):
    code = 0
    if tree.subtree_large is None:
        bits_per_word = math.ceil(math.log(tree.possibilities, 2))
        words_encoding = encode_words(tree.letters, tree.words_valid)
        num_bits = words_encoding[0]
        code_words = words_encoding[1]

        code = (code << 1) + 1
        code = (code << num_bits) | code_words
        code = (code << 3) | 7

    else:
        words_bits = math.floor(math.log(len(tree.words_valid), 2)) + 1
        code = code << words_bits
        code = code + len(tree.subtree_small.words_valid)

        letter_flags = [letter in tree.tree_letter_group for letter in sorted(tree.letters[tree.tree_split_position])][::-1]
        for flag in letter_flags:
            code = code << 1
            if flag:
                code = code + 1

        for i in range(2, -1, -1):
            code = code << 1
            code = code + (tree.tree_split_position >> i) % 2

        code_subtree_small = tree_encoder(tree.subtree_small)
        code_subtree_large = tree_encoder(tree.subtree_large)
        code_bits = 3 + len(tree.letters[tree.tree_split_position]) + words_bits
        code = (code_subtree_small << code_bits) | code
        code_bits = math.floor(math.log(code, 2))
        code = (code_subtree_large << code_bits) | (code - 2**code_bits)
    return code


def encode_123(input):
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    results = ''
    while(input > 0):
        remainder = input % 123
        results = results + foo[remainder]
        input = input // 123
    return(results)

letters_array = [set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)]
words_set = {word for word in words}
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

tree_set = set([tree])
tree_set_all = set()
tree_count = 0
while tree_set:
    tree_count = tree_count + 1
    tree_to_analyze = tree_set.pop()
    if tree_to_analyze.subtree_large:
        tree_set.add(tree_to_analyze.subtree_large)
        tree_set.add(tree_to_analyze.subtree_small)
    tree_set_all.add(tree_to_analyze)

def flatten_letters(letter_groups):
    return tuple(''.join(sorted(letter_group)) for letter_group in letter_groups)

#tree_dict = dict()
file = open('tree_dict.txt', 'rb')
tree_dict = pickle.load(file)
file.close()
for tree in tree_set_all:
    tree_letters = flatten_letters(tree.letters)
    tree_bits = tree.bits_minimum
    if tree.tree_letter_group:
        tree_letter_group = ''.join(sorted(tree.tree_letter_group))
    else:
        tree_letter_group = None
    tree_info = (tree_bits, tree.tree_split_position, tree_letter_group)
    if tree_letters in tree_dict:
        min_bits_seen = tree_dict[tree_letters][0]
        if tree_bits < min_bits_seen:
            print('updating!')
            tree_dict[tree_letters] = tree_info
    else:
        tree_dict[tree_letters] = tree_info

def tree_constructor(tree):
    words_valid = {word for word in words if all(word[i] in tree.letters[i] for i in range(5))}
    flat_letters = flatten_letters(tree.letters)
    if flat_letters in tree_dict:
        tree_split_position = tree_dict[flat_letters][1]
        if tree_split_position is None:
            if tree.parent:
                tree.parent.update_bits_minimum()
        else:
            tree_letter_group = set(tree_dict[flat_letters][2])
            tree.create_subtree(tree_letter_group, tree_split_position)
            tree_constructor(tree.subtree_small)
            tree_constructor(tree.subtree_large)

tree = wordle_tree([set('abcdefghijklmnopqrstuvwxyz') for _ in range(5)], {word for word in words})
tree_constructor(tree)

file = open('tree_dict.txt', 'wb')
pickle.dump(tree_dict, file)
file.close()
tree_code = tree_encoder(tree)
tree_code = tree_code - 2**math.floor(math.log(tree_code, 2))
tree_code_123 = encode_123(tree_code)

print(math.ceil(math.log(tree_code, 2))) # 82664
print(math.ceil(math.log(tree_code, 123))) # 11907
print(tree_code_123)