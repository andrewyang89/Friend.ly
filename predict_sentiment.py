from pathlib import Path

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

from sentiment_analysis import Model
import numpy as np

def run(text):
    """
    Loads the GloVe model and runs the text through the model
    Parameters
    ----------
    text the text to be analyzed

    Returns
    -------
    The predicted sentiment fromm 0-1
    """
    unzipped_folder = "glove.twitter.27B/"  # ENTER THE PATH TO THE UNZIPPED `glove.twitter.27B` HERE

    # use glove2word2vec to convert GloVe vectors in text format into the word2vec text format:
    if not Path('gensim_glove_vectors_200.txt').exists():
        # assumes you've downloaded and extracted the glove stuff
        glove2word2vec(glove_input_file=unzipped_folder + "glove.twitter.27B.200d.txt",
                       word2vec_output_file="gensim_glove_vectors_200.txt")

    # read the word2vec txt to a gensim model using KeyedVectors
    glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors_200.txt", binary=False)

    return predict_sentiment(text, glove_model)

def load_model(self, path):
    """
    Loads the model weights and biases from a .npz file
    Parameters
    ----------
    self the model
    path the path of the .npz file containing the weights and biases

    Returns
    -------
    None
    """
    with open(path, "rb") as f:
        for param, (name, array) in zip(self.parameters, np.load(f).items()):
            param.data[:] = array

def predict_sentiment(text, glove_model):
    """
    Predicts the sentiment of a given piece of text, from 0 (Bad) to 1 (Good)
    Parameters
    ----------
    text the text to be analyzed
    glove_model the model needed to generate 200 length descriptor vectors

    Returns
    -------
    The score from 0-1 of the sentiment
    """
    model = Model()
    load_model(model, "model_two_epochs.npz")
    sentence = text.split()
    arr = np.ones((1, 200, len(sentence))) / 1000000
    for j, word in enumerate(sentence):
        # retrieve glove embedding for every word in sentence
        try:
            arr[0, :, j] = glove_model.get_vector(word.lower())

        # continue if glove embedding not found
        except Exception as e:
            continue
    return model(arr).item()