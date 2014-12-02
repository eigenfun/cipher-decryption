"""
Encapsulates the corpus class
"""

import re
import sys
import textutil
from itertools import izip


MAX_WORDS = 10000


def matches_word(word, partial):
    """
    Checks if a given word could potentially match a partially solved cipher
    """
    for char_word, char_partial in izip(word, partial):
        if char_partial != char_word and char_partial.islower():
            return False
    return True


class CorpusStats(object):
    """
    This class summarizes the corpus statistics necessary for the
    decoding process. It computes the n_letter_words data structure
    which is essentially a dictionary that maps:
    n -> a list of words with n letters that is sorted by word frequency
    """

    def __init__(self, corpus_file):
        """
        The constructor takes the parth to the corpus_file,
        and builds the dictionary n_letter_words.
        """

        print "Reading corpus ..."
        # Words in the corpus
        words = [w.lower() for w in
                 re.split(r'\W+', open(corpus_file).read()) if w.isalpha()]
        print "Read", len(words), "words from corpus \n"
        # Words by their frequency
        word_freq = textutil.word_frequency(words)
        # Words sorted according to their frequency
        words_sorted_by_freq, word_rank = textutil.ranked_frequency(word_freq)
        print "Number of unique words: ", len(words_sorted_by_freq)
        # Not all words in the corpus are probably needed
        self.common_words = words_sorted_by_freq[:MAX_WORDS]
        # Group words by their length so that they can be easily matched as
        # Candidates for ciphers of the same length
        self.n_letter_words = textutil.words_by_n_letters(self.common_words)
        self.word_rank = {w: word_rank[w] for w in self.common_words}

    def get_rank(self, word):
        """Return the frequency rank of a given word"""

        if word in self.word_rank:
            return self.word_rank[word]
        else:
            return sys.maxint

    def candidate_matches(self, partial):
        """Finds all the potential candidates for a partially solved cipher"""

        return [w for w in self.n_letter_words[len(partial)]
                if matches_word(w, partial)][:5]
