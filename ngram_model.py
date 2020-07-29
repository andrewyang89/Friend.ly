import numpy as np
import string
from collections import Counter, defaultdict
import re, string

def unzip(pairs):
    """
    "unzips" of groups of items into separate tuples.

    Example: pairs = [("a", 1), ("b", 2), ...] --> (("a", "b", ...), (1, 2, ...))

    Parameters
    ----------
    pairs : Iterable[Tuple[Any, ...]]
        An iterable of the form ((a0, b0, c0, ...), (a1, b1, c1, ...))

    Returns
    -------
    Tuple[Tuples[Any, ...], ...]
       A tuple containing the "unzipped" contents of `pairs`; i.e.
       ((a0, a1, ...), (b0, b1, ...), (c0, c1), ...)
    """
    return tuple(zip(*pairs))


def normalize(counter):
    """ Convert a `letter -> count` counter to a list
   of (letter, frequency) pairs, sorted in descending order of
   frequency.

    Parameters
    -----------
    counter : collections.Counter
        letter -> count

    Returns
    -------
    List[Tuple[str, int]]
       A list of tuples - (letter, frequency) pairs in order
       of descending-frequency
    """
    total = sum(counter.values())

    return [(char, cnt / total) for char, cnt in counter.most_common()]


def train_lm(text, n):
    """ Train character-based n-gram language model.

    Parameters
    -----------
    text: str
        A string (doesn't need to be lowercased).
    n: int
        The length of n-gram to analyze.

    Returns
    -------
    Dict[str, List[Tuple[str, float]]]
      {n-1 history -> [(letter, normalized count), ...]}
    A dict that maps histories (strings of length (n-1)) to lists of (char, prob)
    pairs, where prob is the probability (i.e frequency) of char appearing after
    that specific history.
    """
    model = defaultdict(Counter)
    length = len(text)
    text = "~" * (n - 1) + text

    for i in range(length):
        history = text[i:i + n - 1]
        char = text[i + n - 1]
        model[history][char] += 1

    for history in model:
        model[history] = normalize(model[history])

    return model

def generate_letter(lm, history):
    """ Randomly picks letter according to probability distribution associated with
    the specified history, as stored in your language model.

    Note: returns dummy character "~" if history not found in model.

    Parameters
    ----------
    lm: Dict[str, List[Tuple[str, float]]]
        The n-gram language model.
        I.e. the dictionary: history -> [(char, freq), ...]

    history: str
        A string of length (n-1) to use as context/history for generating
        the next character.

    Returns
    -------
    str
        The predicted character. '~' if history is not in language model.
    """
    letters, probs = unzip(lm[history])
    prediction = np.random.choice(list(letters), p=list(probs))
    return prediction

def generate_text(lm, n, nletters=100):
    """ Randomly generates `nletters` of text by drawing from
    the probability distributions stored in a n-gram language model
    `lm`.

    Parameters
    ----------
    lm: Dict[str, List[Tuple[str, float]]]
        The n-gram language model.
        I.e. the dictionary: history -> [(char, freq), ...]
    n: int
        Order of n-gram model.
    nletters: int
        Number of letters to randomly generate.

    Returns
    -------
    str
        Model-generated text.
    """

    history = "~" * (n-1)
    output = history
    for i in range(nletters):
        output += generate_letter(lm, history)
        history = output[-(n-1):]
    return output[(n-1):]

punc_regex = re.compile('[{}]'.format(re.escape(string.punctuation)))

def strip_string(corpus):
    """ Removes all punctuation from a string.

        Parameters
        ----------
        corpus : str

        Returns
        -------
        str
            the corpus with all punctuation removed"""
    # substitute all punctuation marks with ""
    return punc_regex.sub('', corpus).lower()

def train_model(path):
    with open(path, "r") as f:
        text = f.read()
    # print(str(len(text)) + " character(s)")
    chars = set(text)
    # print(f"'~' is a good pad character: {'~' not in chars}")
    print('begun training')
    lm = train_lm(text, 11)
    print('finished training')
    return lm

def story(model):
    output = " "
    output = generate_text(lm, 11, 500)
    punctuation = ".,!?';...''``'s"
    words = output.split()

    for n, word in enumerate(words):
        if word in punctuation:
            #         print(words[n-1])
            words[n - 1] += word
            words.pop(n)

    cleaned_words = " ".join(words)
    final = 0
    for n, char in enumerate(cleaned_words[::-1]):
        #     print(n, char)
        if char == '.':
            final = n
            break
    # print(final)
    return cleaned_words[:-final]

lm = train_model('./fairytale_train.txt')
print(story(lm))