import copy
import os
os.chdir(r'C:\Users\Jed\Desktop\Programming\Wordle\Wordle_golf')
import math
import operator as op
from functools import reduce
from collections import Counter

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
        if any([len(letter_set) == 0 for letter_set in letters]):
            raise ValueError('Tried to add letters with no length!', letters)

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


    def add_tree(self, depth_2 = False):
        if len(self.words_valid) == 0:
            self.done = True
        if self.done:
            return
        if self.subtree_large is None:
            if depth_2:
                self.create_depth_2_trees()
            else:
                self.create_best_subtrees()
        else:
            if not self.subtree_large.done:
                self.subtree_large.add_tree(depth_2)
            elif not self.subtree_small.done:
                self.subtree_small.add_tree(depth_2)
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
        desired = round(desired)
        total = round(total)
        if desired > total:
            raise ValueError('Desired > Total', desired, total)

        if desired == 0 or desired == total:
            total_bits = 0
        else:
          #  print('total:', total)
           # print('desired:', desired)
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

    def bit_cross_section(self, letter_set_0, letter_set_1, position_0, position_1):
        words_both = [word for word in self.words_valid if word[position_0] in letter_set_0 and word[position_1] in letter_set_1]
        word_0_only = [word for word in self.words_valid if word[position_0] in letter_set_0 and word[position_1] not in letter_set_1]
        words_not_0 = [word for word in self.words_valid if word[position_0] not in letter_set_0]
        both_bits = wordle_tree.bit_calculator(len(words_both), len(letter_set_0)/len(self.letters[position_0]) * len(letter_set_1)/len(self.letters[position_1]) * self.possibilities)
        only_0_bits = wordle_tree.bit_calculator(len(word_0_only), len(letter_set_0)/len(self.letters[position_0]) * (1 - (len(letter_set_1)/len(self.letters[position_1]))) * self.possibilities)
        not_0_bits = wordle_tree.bit_calculator(len(words_not_0), (1 - len(letter_set_0)/len(self.letters[position_0])) * self.possibilities)
        return both_bits + only_0_bits + not_0_bits

    def create_subtree(self, letter_group, position):
        if position < 0:
            raise ValueError('position must be positive! Given', position)

        letter_group_words_valid = {word for word in self.words_valid if word[position] in letter_group}
        if len(letter_group_words_valid) > 0:
            letter_group_bits = math.ceil(math.log(len(letter_group_words_valid), 2))
        else:
            letter_group_bits = 0
        alternate_group_words_valid = self.words_valid.difference(letter_group_words_valid)
        if len(alternate_group_words_valid) > 0:
            alternate_group_bits = math.ceil(math.log(len(alternate_group_words_valid), 2))
        else:
            alternate_group_bits = 0

        if len(letter_group) + letter_group_bits > (len(self.letters[position]) - len(letter_group)) + alternate_group_bits:
            letter_group = self.letters[position].difference(letter_group)
            letter_group_words_valid = alternate_group_words_valid
            alternate_group_words_valid = self.words_valid.difference(letter_group_words_valid)

        small_subtree_letters = copy.deepcopy(self.letters)
        large_subtree_letters = copy.deepcopy(self.letters)
        small_subtree_letters[position] = letter_group.copy()
        large_subtree_letters[position].difference_update(letter_group)

        self.subtree_small = wordle_tree(small_subtree_letters, letter_group_words_valid, self)
        self.subtree_large = wordle_tree(large_subtree_letters, alternate_group_words_valid, self)
        self.tree_letter_group = letter_group
        self.tree_split_position = position
        self.update_bits_minimum()

    def create_depth_2_trees(self):
        overall_min_bits = self.bits_minimum
        pos_0_best = -1
        pos_1_best = -1
        letter_set_0_best = set()
        letter_set_1_best = set()
        for pos_0 in range(5):
            for pos_1 in range(5):
                if pos_0 != pos_1 and len(self.letters[pos_0]) > 1 and len(self.letters[pos_1]) > 1:
                 #   letter_pair_counts = Counter([word[pos_0] + word[pos_1] for word in self.words_valid])
                 #   letter_pair_max = max(letter_pair_counts, key = letter_pair_counts.get)
                 #   letter_set_0 = set(letter_pair_max[0])
                 #   letter_set_1 = set(letter_pair_max[1])
                    letter_freq_0 = Counter([word[pos_0] for word in self.words_valid])
                    letter_set_0 = {pair[0] for pair in letter_freq_0.most_common(math.ceil(len(self.letters[pos_0])/2))}
                    letter_freq_1 = Counter([word[pos_1] for word in self.words_valid])
                    letter_set_1 = {pair[0] for pair in letter_freq_1.most_common(math.ceil(len(self.letters[pos_1])/2))}
                    done = False
                    overhead_split_0 = 3 + len(self.letters[pos_0]) + math.floor(math.log(len(self.words_valid), 2)) + 1
                    overhead_split_1_always = 3 + len(self.letters[pos_1]) + 1 # not including bits from num_words encoding
                    overhead_leaves = 3 * 4
                    overhead_always = overhead_split_0 + overhead_split_1_always + overhead_leaves
                    if overhead_always < overall_min_bits:
                        start_ent = self.bit_cross_section(letter_set_0, letter_set_1, pos_0, pos_1)
                        continuing_words = [word for word in self.words_valid if word[pos_0] in letter_set_0]
                        min_bits = overhead_always + start_ent + math.floor(math.log(len(continuing_words), 2))
                        while not done:
                            done = True

                            best_new_let_0 = None
                            best_ent_score_0 = min_bits
                            for new_let_0 in self.letters[pos_0].difference(letter_set_0):
                                letter_set_0_extended = letter_set_0.copy().union(new_let_0)
                                ent_score_0 = self.bit_cross_section(letter_set_0_extended, letter_set_1, pos_0, pos_1)
                                continuing_words = [word for word in self.words_valid if word[pos_0] in letter_set_0_extended]
                                ent_score_0 = ent_score_0 + overhead_always + math.floor(math.log(len(continuing_words), 2))
                                if ent_score_0 < best_ent_score_0:
                                    best_new_let_0 = new_let_0
                                    best_ent_score_0 = ent_score_0

                            best_ent_score_1 = min_bits
                            pos_1_counter = Counter([word[pos_1] for word in self.words_valid if word[pos_0] in letter_set_0 and word[pos_1] not in letter_set_1])
                            if len(pos_1_counter) > 0:
                                new_let_1 = max(pos_1_counter, key=pos_1_counter.get)
                                letter_set_1_extended = letter_set_1.copy().union(new_let_1)
                                ent_score_1 = self.bit_cross_section(letter_set_0, letter_set_1_extended, pos_0, pos_1)
                                continuing_words = [word for word in self.words_valid if word[pos_0] in letter_set_0]
                                ent_score_1 = ent_score_1 + overhead_always + math.floor(math.log(len(continuing_words), 2))
                                if ent_score_1 < best_ent_score_1:
                                    best_ent_score_1 = ent_score_1
                                    best_let_1 = new_let_1

                            if min(best_ent_score_0, best_ent_score_1) < min_bits:
                                done = False
                                if best_ent_score_0 < best_ent_score_1:
                                    letter_set_0.add(best_new_let_0)
                                    min_bits = best_ent_score_0
                                else:
                                    letter_set_1.add(best_let_1)
                                    min_bits = best_ent_score_1

                            best_ent_score_0 = min_bits
                            best_let_0 = None
                            if len(letter_set_0) > 1:
                                for new_let_0 in letter_set_0:
                                    letter_set_0_reduced = letter_set_0.copy().difference(new_let_0)
                                    ent_score_0 = self.bit_cross_section(letter_set_0_reduced, letter_set_1, pos_0, pos_1)
                                    continuing_words = [word for word in self.words_valid if word[pos_0] in letter_set_0_reduced] # occasional error
                                    ent_score_0 = ent_score_0 + overhead_always + math.floor(math.log(len(continuing_words), 2))
                                    if ent_score_0 < best_ent_score_0:
                                        best_ent_score_0 = ent_score_0
                                        best_let_0 = new_let_0

                            best_ent_score_1 = min_bits
                            best_let_1 = None
                            if len(letter_set_1) > 1:
                                pos_1_counter = Counter([])
                                pos_1_counter.update({let:0 for let in letter_set_1})
                                pos_1_counter.update([word[pos_1] for word in self.words_valid if word[pos_0] in letter_set_0 and word[pos_1] in letter_set_1])
                                new_let_1 = min(pos_1_counter, key=pos_1_counter.get)
                                letter_set_1_reduced = letter_set_1.copy().difference(new_let_1)
                                ent_score_1 = self.bit_cross_section(letter_set_0, letter_set_1_reduced, pos_0, pos_1)
                                continuing_words = [word for word in self.words_valid if word[pos_0] in letter_set_0]
                                ent_score_1 = ent_score_1 + overhead_always + math.floor(math.log(len(continuing_words), 2))
                                if ent_score_1 < best_ent_score_1:
                                    best_ent_score_1 = ent_score_1
                                    best_let_1 = new_let_1

                            if min(best_ent_score_0, best_ent_score_1) < min_bits:
                                done = False
                                if best_ent_score_0 < best_ent_score_1:
                                    letter_set_0.remove(best_let_0)
                                    min_bits = best_ent_score_0
                                else:
                                    letter_set_1.remove(best_let_1)
                                    min_bits = best_ent_score_1
                        if min_bits < overall_min_bits:
                            overall_min_bits = min_bits
                            pos_0_best = pos_0
                            pos_1_best = pos_1
                            letter_set_0_best = letter_set_0.copy()
                            letter_set_1_best = letter_set_1.copy()
        if overall_min_bits < self.bits_minimum:
            self.create_subtree(letter_set_0_best, pos_0_best)
        else:
            self.create_best_subtrees()

    def create_best_subtrees(self):
        min_bits = self.bits_minimum + 1
        letter_best = ''
        index_best = -1
        for i in range(len(self.letters)):
            letters_ordered = ''.join(sorted([letter for letter in self.letters[i]], 
                                              key = lambda key: len([word for word in self.words_valid if word[i] == key]))[::-1])
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
        else:
            self.done = True

    def bits_overhead(self):
        #position split + letters_splitting + num_words to subtree_small + 1 (to cap the string)
        return 3 + len(self.letters[self.tree_split_position]) + math.floor(math.log(len(self.words_valid), 2)) + 1

    def update_bits_minimum(self):
        bits_subtrees = self.subtree_small.bits_minimum + self.subtree_large.bits_minimum
        self.bits_minimum = self.bits_overhead() + bits_subtrees
        if self.parent:
            self.parent.update_bits_minimum()

        else:
            print(self.bits_minimum)
