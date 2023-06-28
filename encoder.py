import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')

from wordle_tree import wordle_tree
import math
import operator as op
from functools import reduce

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
    # print("letter_sets:", [''.join(sorted(letter_set)) for letter_set in letter_sets])
    # print("words:", words)
    # print("num_words:", len(words))
    # print("bits_per_word:", bits_per_word)
    # print("\n")
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
    #print('start indexes_to_words')
    result_words = []
    for i in range(len(word_indexes)):
        word_num = word_indexes[i]
        start_word_num = word_num

        word = ''
        for j in range(len(letter_groups)):
            letter_index = word_num // place_per_position[j] # 16916
            word = word + letter_groups[j][letter_index]
            word_num = word_num % place_per_position[j]
        result_words.append(word)
        if word in {'aajed', 'scacs', 'aulcs'}:
            print('start_word_num', start_word_num)
            print('word:', word)
            print('word_num', word_num)
            print('letter_groups', letter_groups)
            print('place_per_position', place_per_position)
    #print('end indexes_to_words')
    return(result_words)

#(subtree_large)(subtree_small)(words in subtree_small)(letter_flags)(split_position)
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
        #  print('letter_groups:', [''.join(sorted(tree.letters[i])) for i in range(len(tree.letters))])
        #  print('word_count:', len(tree.words_valid))
        #  print(sorted(tree.words_valid))
        #  print('')

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
        code_bits = math.floor(math.log(code, 2)) + 1
        code = (code_subtree_large << code_bits) | code
    return code


def encode_249(input):
    foo = '	 !"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
    results = ''
    while(input > 0):
        remainder = input % 249
        results = results + foo[remainder]
        input = input // 249
    return(results)

vowels = set('aeiou')
consonants = set('bcdfghjklmnpqrstvwxyz')
large_letters_array = [0] * 32
tree_array = [0] * 32
codes_array_raw = [0] * 32
word_counts = [0] * 32
for i in range(32):
    letters_array = [vowels.copy() if (i >> j) & 1 else consonants.copy() for j in range(5)]
    words_valid = {word for word in words if all([word[j] in letters_array[j] for j in range(5)])}
    word_counts[i] = len(words_valid)
    tree = wordle_tree(letters_array, words_valid)
    counter = 0
    while not tree.done:
        counter = counter + 1
        tree.add_tree()
    codes_array_raw[i] = tree_encoder(tree)
    tree_array[i] = tree

codes_array = [encode_249(code) for code in codes_array_raw]
word_count_bits_max = math.ceil(math.log(max([word_count for word_count in word_counts]), 2))
words_per_tree_code_raw = 0
for i in reversed(range(32)):
    words_per_tree_code_raw = words_per_tree_code_raw * 2**12 + word_counts[i]
words_per_tree_code = encode_249(words_per_tree_code_raw)

