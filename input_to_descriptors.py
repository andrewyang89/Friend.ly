
import numpy as np
import re, string
from collections import Counter
from database import Database


entries = Database.biographies

# these need to be imported from the input file
new_name = name
new_entry = entry
entries.append(entry)


punc_regex = re.compile('[{}]'.format(re.escape(string.punctuation)))

def strip_punc(corpus):
    """ Removes all punctuation from a string.

        Parameters
        ----------
        corpus : str

        Returns
        -------
        str
            the corpus with all punctuation removed"""
    # substitute all punctuation marks with ""
    return punc_regex.sub('', corpus)


def to_counter(doc):
    """ 
    Produce word-count of document, removing all punctuation
    and making all the characters lower-cased.
    
    Parameters
    ----------
    doc : str
        input text
    
    Returns
    -------
    collections.Counter
        lower-cased word -> count"""

    return Counter(strip_punc(doc).lower().split())


def to_idf(vocab, counters):
    """ 
    Given the vocabulary, and the word-counts for each document, computes
    the inverse document frequency (IDF) for each term in the vocabulary.
    
    Parameters
    ----------
    vocab : Sequence[str]
        Ordered list of words that we care about.

    counters : Iterable[collections.Counter]
        The word -> count mapping for each document.
    
    Returns
    -------
    numpy.ndarray
        An array whose entries correspond to those in `vocab`, storing
        the IDF for each term `t`: 
                           log10(N / nt)
        Where `N` is the number of documents, and `nt` is the number of 
        documents in which the term `t` occurs.
    """
    N = len(counters)
    nt = [sum(1 if t in counter else 0 for counter in counters) for t in vocab]
    nt = np.array(nt, dtype=float)
    return np.log10(N/nt)




def to_tf(counters, vocab):
    """
    Parameters
    ----------
    counters : collections.Counter
        The word -> count mapping for each input.
    vocab : Sequence[str]
        Ordered list of words that we care about.
    
    Returns
    -------
    numpy.ndarray
        The TF descriptor for each document, whose components represent
        the frequency with which each term in the vocab occurs
        in the given document."""
    tfs = list()
    for counter in counters:
        x = np.array([counter[word] for word in vocab], dtype=float)
        tfs.append(x / x.sum())

    return np.vstack(tfs)


def to_vocab(counters, stop_words=tuple()):
    """ 
    [word, word, ...] -> sorted list of top-k unique words
    Excludes words included in `stop_words`
    
    Parameters
    ----------
    counters : Iterable[Iterable[str]]
    
    k : Optional[int]
        If specified, only the top-k words are returned
    
    stop_words : Collection[str]
        A collection of words to be ignored when populating the vocabulary
    """
    vocab = Counter()
    for counter in counters:
        vocab.update(counter)
        
    for word in set(stop_words):
        vocab.pop(word, None)
    return sorted(i for i in vocab if i not in stop_words)


def compute_descriptors(all_entries):
    """
    Computes tf_idf descriptors for all entries.
    
    Parameters
    ----------
    all_entries: List[str]
    
    Returns
    -------
    tf_idf: numpy array -> shape(len(all_inputs), len(vocab))
    """
    word_counts = list()
    for entry in all_entries:
        word_counts.append(to_counter(entry))
    vocab = to_vocab(word_counts, stop_words=stops)
    idfs = to_idf(vocab, word_counts)
    tfs = to_tf(word_counts, vocab)
    tf_idf = tfs * idfs
    return tf_idf
    

with open("./stopwords.txt", 'r') as r:
    stops = []
    for line in r:
        stops += [i.strip() for i in line.split('\t')]

descriptors = compute_descriptors(entries)
Database.add_profile(new_name, entry, descriptors[-1])

