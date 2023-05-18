import re
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Ngram:
    words: Tuple[str]

    def __hash__(self):
        #return hash(self.words)
        h = 0
        for i, word in enumerate(self.words):
            for j, letter in enumerate(word):
                h = 37 * h + ord(letter) + i + j
        return h

def make_ngrams(string, n=5):
    """Return all n-grams of a given string (default n=5)."""

    # Split the string into lower-case words
    words = re.split("\\W", string.lower())
    words = [word for word in words if len(word) > 0]

    # Produce the n-grams
    ngrams = [ words[i:i+n] for i in range(len(words)) ]
    # The last few words in the string will give "n-grams" of length
    # less than n - remove them
    ngrams = [ ngram for ngram in ngrams if len(ngram) == n ]

    return [ Ngram(tuple(ngram)) for ngram in ngrams ]
