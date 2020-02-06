# Based on MarkoviPy:
# https://pypi.org/project/markovipy/
# GNU General Public License v3

import string
import codecs
import re
import os
import random
import collections

PUNCTUATIONS = string.punctuation


def get_word_list(file):
    """Get a list of words by tokenising the user's file"""

    # tokenizer = nltk.tokenize.casual.TweetTokenizer()

    try:
        with codecs.open(file, 'r', encoding='utf-8') as f:
            # words_list = tokenizer.tokenize(f.read())
            # or use a regex
            words_list = [w for w in re.findall(r"[\w']+|[\".,!'?;\-:]", f.read())]
        return words_list
    except OSError:
        return "File not found. Please check the given path."

class Markov:
    def __init__(self, filename="", markov_length=3):
        self.starting_words = []  # keep track of sentence-beginning words
        self.middle_mapping = collections.defaultdict(collections.Counter)
        self.final_mapping = {}
        self.markov_length = markov_length
        if os.path.exists(filename):
            self.filename = filename
        else:
            raise FileNotFoundError("Please enter a valid corpus filename.")
        self.words_list = get_word_list(self.filename)

    def normalise_mapping(self):
        for word_tuple, probable_word in self.middle_mapping.items():
            total = sum(probable_word.values())
            self.final_mapping[word_tuple] = dict([(k, v / total) for k, v in probable_word.items()])

    def _build_middle_mapping(self, word_history, next_word):
        while len(word_history) > 0:
            key = tuple(word_history)
            self.middle_mapping[key][next_word] += 1.0
            word_history = word_history[1:]

    def _iterate_through_word_list(self):
        self.starting_words.append(self.words_list[0])
        for i in range(1, len(self.words_list) - 1):
            if i < self.markov_length:
                word_history = self.words_list[:i + 1]
            elif i >= self.markov_length:
                word_history = self.words_list[i - self.markov_length + 1:i + 1]
            next_word = self.words_list[i + 1]
            if word_history[-1] == "." and next_word not in list(PUNCTUATIONS):
                self.starting_words.append(next_word)

            self._build_middle_mapping(word_history, next_word)

        self.normalise_mapping()

    def _next(self, prev_list):
        probability_sum = 0.0
        next_word = ""
        index = random.random()
        while tuple(prev_list) not in self.final_mapping:
            prev_list.pop(0)
        for k, v in self.final_mapping[tuple(prev_list)].items():
            probability_sum += v
            if probability_sum >= index and next_word == "":
                next_word = k
                break
        return next_word

    def generate_sentence(self):
        self._iterate_through_word_list()
        current_word = random.choice(self.starting_words)
        sent = current_word.capitalize()
        prev_list = [current_word]
        while (current_word != "."):
            current_word = self._next(prev_list)
            prev_list.append(current_word)
            if len(prev_list) > self.markov_length:
                prev_list.pop(0)
            if (current_word not in list(".,-\"!?;")):
                sent += " "
            sent += current_word
        return sent
