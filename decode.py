"""
Entry point into the decryption process. It handles the command-line interface
and file i/o processing
"""

import sys
import textutil
from corpus import CorpusStats
from cipher import CipherText
from solver import Solver


def main():
    """
    Entry point into the decryption process
    """

    # If the corpus and encoded file paths are not provided in the
    # command line arguments, pick the default files
    if len(sys.argv) < 3:
        print """
        Assuming default paths for the corpus and encrypted files:
        ./corpus-en.txt' and ./encoded-en.txt.

        If they are located somewhere else, please run the script
        with command-line arguments specifying the file locations.
        For example:

        python ./decode.py ./data/corpus-en.txt ./data/encoded-en.txt
        """

        corpus_file = 'corpus-en.txt'
        encrypted_file = 'encoded-en.txt'
    else:
        corpus_file, encrypted_file = sys.argv[1], sys.argv[2]

    # Read the encoded file and the corpus
    cipher_txt = CipherText(encrypted_file)
    corpus = CorpusStats(corpus_file)
    solver = Solver(cipher_txt, corpus)
    # Compute the solution
    best_solution = solver.solve(corpus)

    print """
    Writing the decrypted text to file:
    ./decoded.txt

    the best solution key to file:
    ./decryption_cipher.txt

    original encryption key to file:
    ./encryption_cipher.txt
    """

    # Write the solutions
    file_decrypt_cipher = open("decryption_cipher.txt", 'w')
    file_encrypt_cipher = open("encryption_cipher.txt", 'w')
    for char in textutil.A2Z:
        if char in best_solution:
            file_decrypt_cipher.write(
                char + ' -> ' + best_solution[char] + '\n')
            file_encrypt_cipher.write(
                best_solution[char] + ' -> ' + char + '\n')
        else:
            file_decrypt_cipher.write(char + ' -> ?' + '\n')
            file_encrypt_cipher.write('? -> ' + char + '\n')

    file_decrypt_cipher.close()
    file_encrypt_cipher.close()
    cipher_txt.decode(best_solution, 'decoded.txt')

if __name__ == "__main__":
    main()
