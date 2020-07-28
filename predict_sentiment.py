from pathlib import Path

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

from .sentiment_analysis import Model
import numpy as np

def run(text):
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
    with open(path, "rb") as f:
        for param, (name, array) in zip(self.parameters, np.load(f).items()):
            param.data[:] = array

def predict_sentiment(text, glove_model):
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