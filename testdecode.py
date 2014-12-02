"""
Tests for the decryption process
"""

import unittest
import textutil
from corpus import CorpusStats
from cipher import CipherText
from solver import Solver

class TestDecode(unittest.TestCase):
    """
    Test suite that exercises the decryption process using 2 encrypted texts:
    The poem Raven and selected quotes.
    """

    def setUp(self):
        """
        Initialize the test suite. Set up the file paths for the
        plain text and randomly encrypted version of it
        """

        self.raven_poem = {
            'plain': './data/raven.txt', 'encoded': './data/raven.txt-enc'
        }
        self.greatness_quotes = {
            'plain': './data/quotes.txt', 'encoded': './data/quotes.txt-enc'
        }
        self.corpus_file = './data/corpus-en.txt'

    def compare_text(self, files):
        """
        Compares the original plain text with the decrypted one
        """

        plain_txt = CipherText(files['plain'])
        cipher_txt = CipherText(files['encoded'])
        corpus = CorpusStats(self.corpus_file)
        solver = Solver(cipher_txt, corpus)

        best_solution = solver.solve(corpus)

        def clean(w_list):
            """
            Cleans up white spaces
            """
            return [w.strip(' \r\t') for w in w_list if w.strip(' \r\t')]

        w_enc = clean(cipher_txt.words)
        w_dec = clean(plain_txt.words)


        n_solved = 0.0
        for encoded, actual in zip(w_enc, w_dec):
            decoded = textutil.decode_word(encoded, best_solution)
            if decoded == actual:
                n_solved += 1.0
            else:
                print "Mismatch! Expected: ", actual, "but got: ", decoded

        return n_solved, len(cipher_txt.words)

    def test_raven(self):
        """
        The first test case that uses encrypted poem raven
        """

        n_solved, total = self.compare_text(self.raven_poem)
        self.assertAlmostEqual(n_solved/total, 0.99, 1)

    def test_greatness_quotes(self):
        """
        The second test case that uses randomly encrypted quotes
        """

        n_solved, total = self.compare_text(self.greatness_quotes)
        self.assertAlmostEqual(n_solved/total, 0.99, 1)

if __name__ == '__main__':
    unittest.main()
