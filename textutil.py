"""
A collection of useful functions to help processing the text for deciphering
"""

### A convenient list of letters a-z
A2Z = [chr(x) for x in range(ord('a'), ord('z') + 1)]


def has_upper(word):
    """
    Checks if the word w has an uppercase character
    indicating that it's a partially solved word
    """
    for letter in word:
        if letter.isupper():
            return True
    return False


def decode_char(char, letter_map):
    """Decodes a character based on the mapping"""
    return letter_map[char.lower()] \
        if char.islower() else letter_map[char.lower()].upper()


def uncoded(char, uncoded_char='?'):
    """Checks if a given character is coded or not"""
    if char.lower() in A2Z:
        return uncoded_char
    else:
        return char


def decode_word(cipher, letter_map):
    """Decode a word based on the given map"""
    return ''.join(letter_map[char]
                   if char in letter_map else char.upper() for char in cipher)


def word_frequency(word_list):
    """Computes frequency of words in the given list"""
    word_freq = {}
    for word in word_list:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq


def ranked_frequency(word_freq):
    """Ranks words based on frequency"""
    words = sorted(word_freq.keys(), key=word_freq.get, reverse=True)
    ranks = {w: rank for rank, w in enumerate(words)}
    return words, ranks


def words_by_n_letters(word_list):
    """Groups words by length"""
    n_letters = {}
    for word in word_list:
        w_len = len(word)
        if w_len in n_letters:
            n_letters[w_len].append(word)
        else:
            n_letters[w_len] = [word]
    return n_letters
