"""
Encapsulates the deciphering algorithm in the
main class Solver and helper methods
"""

from random import shuffle
import textutil

N_SHUFFLE = 2  # Number of times to shuffle words to match


def get_update(enc, candidate, new_map):
    """Computes new mapping based on a candidate word"""

    # Align all the candidates with the encoded cipher
    # and extract the mapping between encoded to original by
    # matching letters in the same position
    map_updates = {}
    for encoded, cnd_word in zip(enc, candidate):
        if encoded.islower():
            continue
        enc_lower = encoded.lower()
        if enc_lower in new_map or enc_lower in map_updates \
                or cnd_word in new_map.values() \
                or cnd_word in map_updates.values():
            return {}
        map_updates[encoded.lower()] = cnd_word
    return map_updates


def infer_mapping(clues, mapping, n_shuffle=N_SHUFFLE):
    """Infers new mapping based on available clues and current mapping"""

    # Apply the current mapping to generate new mapping guesses
    guesses = []
    for _ in range(n_shuffle):
        new_map = mapping.copy()

        for enc, candidates in clues:
            for cnd in candidates:
                map_updates = get_update(enc, cnd, new_map)
                if map_updates:
                    new_map.update(map_updates)
                    break
        guesses.append(new_map)
        shuffle(clues)
    return guesses


class Solver(object):
    """
    Encapsulates the decryption algorithm
    """

    def __init__(self, cipher, corpus):
        """
        The constructor takes an instance of
        the CipherText that needs to be decrypted
        """

        self.cipher = cipher
        self.corpus = corpus
        self.ranked_cipher = cipher.ranked_cipher
        self.num_unique_ciphers = len(self.ranked_cipher)
        self.best_mapping, self.best_score = None, 0

    def score_mapping(self, solution_key):
        """
        Scores a given solution_key
        """

        def word_score(word):
            """Scores a given word based on completion"""

            word_len, completed = len(word), 0.0
            if word_len == 0:
                return 0.0
            for char in word:
                if char.islower():
                    completed += 1.0
            completed /= word_len
            if completed > 0.99:
                return 1.0
            else:
                return 0.0

        completed, decoded = 0.0, self.cipher.apply_mapping(solution_key)
        for dec in decoded:
            w_score = word_score(dec)
            completed += 1.0 if w_score > 0.99 else 0.0
        return completed / self.num_unique_ciphers

    def get_best_guess(self, n_candidates,
                       candidate_groups, candidate_map, current_map):
        """
        Computes the best score by matching the encoded
        with the word candidates
        """

        # Generate clues based on candidate word matches for encoded words
        ez_encoded, ez_candidates = [], []
        for n_candidate in n_candidates:
            for enc in candidate_groups[n_candidate]:
                ez_encoded += [enc]
                candidates = sorted(candidate_map[enc],
                                    key=lambda c: self.corpus.word_rank[c])
                ez_candidates.append(candidates)
            clues = sorted(zip(ez_encoded, ez_candidates),
                           key=lambda clue: self.corpus.word_rank[clue[1][0]])
            # Use the clues to infer mapping guesses
            updated_guesses = infer_mapping(clues, current_map)
            # Score the different guess mapping and sort them
            guess_scores = sorted([(guess, self.score_mapping(guess))
                                   for guess in updated_guesses],
                                  key=lambda x: x[1], reverse=True)
            best_guess = guess_scores[0]
            return best_guess

    def update_guess(self, current_map, unsolved=None):
        """
        Updates the current guess as captured in the current_map by
        inferring and scoring new guesses based on match candidates
        """

        if not unsolved:
            unsolved = [w for w in self.cipher.apply_mapping(current_map)
                        if textutil.has_upper(w)]

        candidate_map = {w: self.corpus.candidate_matches(w)
                         for w in unsolved}

        if not candidate_map:
            return None, None

        # Include negated words in the form of un + <word> / in + <word>
        # to be matched as they may not be well represented in the corpus
        negated_words = {}
        if not any(candidate_map.values()):
            for key, val in candidate_map.items():
                if not val and key[:2] in ('un', 'in'):
                    negated_words[key[2:]] = \
                        self.corpus.candidate_matches(key[2:])
            if not negated_words:
                return None, None
        candidate_map.update(negated_words)

        candidate_map = {k: v for k, v in candidate_map.items() if v}
        n_candidates = set(len(v) for v in candidate_map.values())
        candidate_groups = {k: [] for k in sorted(n_candidates)[:5]}

        for key, val in candidate_map.items():
            if len(val) in candidate_groups:
                candidate_groups[len(val)] += [key]

        n_candidates = sorted(n_candidates)

        return self.get_best_guess(n_candidates,
                                   candidate_groups,
                                   candidate_map, current_map)

    def unsolved_part(self, solution_key):
        """Unsolved ciphers remaining after applying the solution_key"""

        char_unmapped = set(textutil.A2Z) - set(solution_key.keys())
        decoded = self.cipher.apply_mapping(solution_key)
        unsolved = [w for w in decoded if textutil.has_upper(w)]
        return char_unmapped, unsolved

    def solve(self, target_score=1.0):
        """
        Entry point into the solution process. It initializes the first
        guess by matching the most frequent word in the
        corpus to the most frequent cipher word.
        """

        most_common_cipher = self.ranked_cipher[0]
        # Find the counterpart for the most common word in the cipher text
        guess_most_common_cipher = self.corpus.n_letter_words[
            len(most_common_cipher)][0]
        # Generate the initial character mapping from this initial guess
        mapping_guess = dict(zip(most_common_cipher,
                                 guess_most_common_cipher))
        score = 0.0
        unsolved = None
        # Progressively generate new guesses from the current guess
        # until the target score is reached or we run out of
        # characters to map
        while len(mapping_guess) > 0 and score < target_score:
            mapping_guess, score = self.update_guess(
                mapping_guess, unsolved)
            free_chars, unsolved = self.unsolved_part(mapping_guess)
            if len(free_chars) == 0 or len(unsolved) == 0:
                break
        return mapping_guess
