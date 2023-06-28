import copy
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
import math
from utilities import ncr
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

class wordle_tree:
    def __init__(self, letters, words_valid, parent = None):
        self.letters = letters
        self.words_valid = words_valid
        self.possibilities = self.find_possibilities()
        self.bits_minimum = self.find_bits()
        #self.branching_bits_penalty = 30
        self.subtree_large = None
        self.subtree_small = None
        self.parent = parent
        self.tree_split_position = None
        self.tree_letter_group = None
        self.done = False
        for i in range(5):
            for word in words_valid:
                if word[i] not in letters[i]:
                    raise ValueError('impossible word present', letters, word, self)


    def add_tree(self):
        if len(self.words_valid) == 0:
            self.done = True
        if self.done:
            return
        if self.subtree_large is None:
            self.create_best_subtrees()
        else:
            if not self.subtree_large.done:
                self.subtree_large.add_tree()
            elif not self.subtree_small.done:
                self.subtree_small.add_tree()
            else:
                self.done = True


    def find_possibilities(self):
        possibilities = 1
        for i in range(len(self.letters)):
            possibilities = possibilities * len(self.letters[i])
        return possibilities


    def find_bits(self):
        return math.ceil(wordle_tree.bit_calculator(len(self.words_valid), self.possibilities) + 4)

    @classmethod
    def bit_calculator(self, desired, total):
        if desired > total:
            raise ValueError('Desired > Total', desired, total)

        if desired == 0 or desired == total:
            total_bits = 0
        else:
          #  print('total:', total)
           # print('desired:', desired)
            total = int(total)
            desired = int(desired)
            total_bits = math.ceil(math.log(ncr(total, desired), 2))
           # total_bits = -(desired * math.log(desired/total, 2) + (total - desired) * math.log((total - desired)/total, 2))
        return total_bits

    @classmethod
    def bit_extended_calculator(self, desired, total, desired_g1, total_g1):
        if desired - desired_g1 > total - total_g1:
            raise ValueError(desired, total, desired_g1, total_g1)
        bits_g1 = math.ceil(wordle_tree.bit_calculator(desired_g1, total_g1))
        bits_g2 = math.ceil(wordle_tree.bit_calculator(desired - desired_g1, total - total_g1))
        return bits_g1 + bits_g2

    def create_subtree(self, letter_group, position):
        small_subtree_words_valid = {word for word in self.words_valid if word[position] in letter_group}
        large_subtree_words_valid = self.words_valid.difference(small_subtree_words_valid)
        small_subtree_letters = copy.deepcopy(self.letters)
        small_subtree_letters[position] = letter_group
        large_subtree_letters = copy.deepcopy(self.letters)
        large_subtree_letters[position].difference_update(letter_group)
        self.subtree_small = wordle_tree(small_subtree_letters, small_subtree_words_valid, self)
        self.subtree_large = wordle_tree(large_subtree_letters, large_subtree_words_valid, self)
        self.tree_letter_group = letter_group
        self.tree_split_position = position

    def create_best_subtrees(self):
        min_bits = self.bits_minimum + 1
        letter_best = ''
        index_best = -1
        for i in range(len(self.letters)):
            letters_ordered = ''.join(sorted([letter for letter in self.letters[i]], 
                                              key = lambda key: len([word for word in words if word[i] == key]))[::-1])
            for j in range(len(letters_ordered)):
                letter_group = letters_ordered[:j]
                words_sublist_count = len([word for word in self.words_valid if word[i] in letter_group])
                subtree_bit_count =  wordle_tree.bit_extended_calculator(
                                                    len(self.words_valid),
                                                    self.possibilities,
                                                    words_sublist_count,
                                                    len(letter_group) * self.possibilities / len(self.letters[i]))
                subtree_bit_count = subtree_bit_count + 8 + 3 + len(self.letters[i]) + math.floor(math.log(len(self.words_valid), 2)) + 1
                if subtree_bit_count < min_bits:
                   # print(i, letter_group, words_sublist_count)
                    min_bits = subtree_bit_count
                    letter_group_best = letter_group
                    index_best = i
        if min_bits <= self.bits_minimum:
            letter_group_set = {letter for letter in letter_group_best}
            self.create_subtree(letter_group_set, index_best)
            self.update_bits_minimum(math.ceil(min_bits))
        else:
            self.done = True

    def update_bits_minimum(self, bits_minimum_new):
        bits_difference = self.bits_minimum - bits_minimum_new
        self.reduce_bits(bits_difference)

    def reduce_bits(self, bits_difference):
        self.bits_minimum = self.bits_minimum - bits_difference
        if self.parent:
            self.parent.reduce_bits(bits_difference)
        else:
            print(self.bits_minimum)
