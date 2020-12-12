import tensorflow as tf
from tensorflow import keras

# Utility file where variables life that are used in 'model.py' and 'main.py'

# Get movie review data from keras
data = keras.datasets.imdb

# Load data with only the words that occur at least 10000 times
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=10000)

# Get word index of the data and add our own 'helper' words to the list
word_index = data.get_word_index()
word_index = {k: (v+3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3
