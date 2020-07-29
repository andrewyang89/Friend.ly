import numpy as np
import re, string
import camera
from collections import Counter
from database import Database
from recognize_speech import recognize_speech_record


num_people = 10

with open("./stopwords.txt", 'r') as r:
    stops = []
    for line in r:
        stops += [i.strip() for i in line.split('\t')]

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


def to_idf(N, counters):
    """
    Computes the inverse document frequency (IDF) from the total word count.

    Parameters
    ----------
    N: int
        total number of documents

    counters : Iterable[collections.Counter]
        The word -> count mapping for all documents.

    Returns
    -------
    dictionary mapping each word to IDF.
    """
    return {word: np.log10(N / (1 + count)) for word, count in counters.items() if word not in stops}


def to_vocab(old_vocab, stop_words=tuple()):
    """
    Sorts vocab and excludes words included in `stop_words`

    Parameters
    ----------
    old_vocab : List[str]
        Old vocab to filter and sort

    stop_words : Collection[str]
        A collection of words to be ignored when populating the vocabulary
    """
    return sorted(i for i in old_vocab if i not in stop_words)


def to_tf(counter, vocab):
    """
    Parameters
    ----------
    counter : collections.Counter
        The word -> count mapping for all vocab.
    vocab : Sequence[str]
        Ordered list of words that we care about.

    Returns
    -------
    numpy.ndarray
        The TF descriptor for each document, whose components represent
        the frequency with which each term in the vocab occurs
        in the given document."""

    x = np.array([counter[word] for word in vocab], dtype=float)
    return x / x.sum()


def compute_descriptors(all_entries):
    """
    Computes tf_idf descriptors for all entries.

    Parameters
    ----------
    all_entries: List[str]

    Returns
    -------
    all_weights: numpy array -> shape(len(all_inputs), len(vocab))
    """
    word_counts = Counter()
    tfs = list()
    for entry in all_entries:
        word_counts.update(to_counter(entry))

    vocab = to_vocab(word_counts.keys(), stop_words=stops)

    for entry in all_entries:
        tfs.append(to_tf(to_counter(entry), vocab))

    tfs = np.vstack(tfs)
    idfs = list(to_idf(len(all_entries), word_counts).values())
    tf_idf = tfs * idfs

    return tf_idf

def new_person(db):
    names = db.names
    # contacts = db.contacts
    entries = db.biographies
    new_name = input("Please enter your name: ")
    # new_contact = input("Please enter your contact")
    # connect to audio to text file
    new_entry = recognize_speech_record("Tell us a bit about yourself: ")
    names.append(new_name)
    # contacts.append(new_contact)
    entries.append(new_entry)

    descriptors = compute_descriptors(entries)

    print ("Taking a picture. Smile!")
    pic = camera.take_picture()
    db.add_and_update_profiles(names, entries, descriptors)
    db.update_one_profile(new_picture=pic)

# for i in range(num_people):
#     new_person()
#
# db.save('loaded_10_people.pkl')

# db.load('loaded_10_people.pkl')
# print(db.names)