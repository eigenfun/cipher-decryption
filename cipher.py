"""
Encapsulates the cipher text class
"""

import re
import textutil


class CipherText(object):
    """
    This class represents the encrypted text to be decoded
    """

    def __init__(self, filename):
        """
        The constructor takes the path to the encrypted file,
        and computes the cipher stats.
        """

        print "Cipher Text: ", filename
        self.encoded = open(filename).read()
        self.words = [w.lower() for w in
                      re.split(r"\W+", self.encoded)]

        self.cipher_freq = textutil.word_frequency(self.words)
        self.ranked_cipher, self.cipher_rank = textutil.ranked_frequency(
            self.cipher_freq)


    def apply_mapping(self, solution_key):
        """Decodes the cipher text based on the given letter mapping"""

        return [textutil.decode_word(c, solution_key)
                for c in self.ranked_cipher]

    def decode(self, letter_map, filename=None):
        """
        Decodes the encrypted text with the solution
        key provided by the letter_map
        """

        decoded = ''.join(textutil.decode_char(enc, letter_map)
                          if enc.lower() in letter_map
                          else textutil.uncoded(enc)
                          for enc in self.encoded)

        if filename is None:
            return decoded.splitlines()

        f_handle = open(filename, 'w')
        f_handle.write(decoded)
        f_handle.close()
