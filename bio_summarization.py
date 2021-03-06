import re, string
import numpy as np
import nltk
from collections import Counter

punc_regex = re.compile('[{}]'.format(re.escape(string.punctuation + '’')))


def load_stop_words():
    with open("./stopwords.txt", 'r') as r:
        stops = []
        for line in r:
            stops += [i.strip() for i in line.split('\t')]
    return stops


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
    
    Returns
    -------
    collections.Counter
        lower-cased word -> count"""
    return Counter(strip_punc(doc).lower().split())


def to_vocab(name, counters, k=None, stop_words=tuple()):
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
    for n in name.lower().split():
        if n in vocab:
            del vocab[n]
    for word in set(stop_words):
        vocab.pop(word, None)  # if word not in bag, return None
    return sorted(i for i,j in vocab.most_common(k))


def to_tf(counter, vocab):
    """
    Parameters
    ----------
    counter : collections.Counter
        The word -> count mapping for a document.
    vocab : Sequence[str]
        Ordered list of words that we care about.
    
    Returns
    -------
    numpy.ndarray
        The TF descriptor for the document, whose components represent
        the frequency with which each term in the vocab occurs
        in the given document."""
    x = np.array([counter[word] for word in vocab], dtype=float)
    return x / x.sum()


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
    return np.log10(N / nt)


def get_tf_idfs(name, entries):
    word_counts = [to_counter(doc) for doc in entries]
    vocab = to_vocab(name, word_counts, stop_words=load_stop_words())
    tfs = np.vstack([to_tf(counter, vocab) for counter in word_counts])
    idf = to_idf(vocab, word_counts)
    return tfs * idf, vocab


def summarize_doc(name, db, bio_length=10):
    """
    Summarize particular person's biography into keywords

    Parameters
    ----------
    name : str
        person to summarize biography
    db : Database
        Database object to retreive biographies from
    bio_length : int
        Number of keywords in final shortened biography
    """
    entries = db.biographies
    person = db.names.index(name)
    name = db.names[person]
    tf_idfs, vocab = get_tf_idfs(name, entries)
    max_indices = (-tf_idfs[person]).argsort()
    nouns = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(db.biographies[person])) if pos[0] == 'N']
    bio = []
    for word in [vocab[x] for x in max_indices]:
        if len(bio) >= min(bio_length, len(nouns)):
            break
        if word in nouns:
            bio.append(word)
    return ', '.join(bio)