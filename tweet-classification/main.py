import tensorflow as tf
from util import word_index


# This is a script for testing the trained model for text classification from the
# model.py script.


# Get the reverse word index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])


def decode(array):
    """
    Decodes the passed array. This means that the encoded words from the array are mapped
    to their referenced values in the word_index dictionary.
    Example: in: [3244, 345, 4, 23444]   out: ["this", "is", "a", "test"]

    Args:
        array: The array with all the encoded words that need to be decoded.

    Returns:
        The decoded array.
    """
    return " ".join([reverse_word_index.get(i, "?") for i in encoded_tweet])


def encode(array):
    """
    Encodes the passed array. This means that the words from the array are mapped
    to their referenced values in the word_index dictionary.
    Example: in: ["this", "is", "a", "test"]   out: [3244, 345, 4, 23444]

    Args:
        array: The array with all the words that need to be encoded.

    Returns:
        The encoded array.
    """
    encoded = [1]
    for word in tweet:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


# Load the model
model = tf.keras.models.load_model('text-classification-blob.h5')

tweet = 'This is really a bad day to buy stocks. I think this is the worst day since a long time.'
tweet = tweet.replace(".", "").replace(",", "").replace(":", "").split()
encoded_tweet = encode(tweet)
encoded_tweet = tf.keras.preprocessing.sequence.pad_sequences([encoded_tweet], value=word_index["<PAD>"], padding="post",
                                                           maxlen=100)

# Predict the value and print to standard output
predict = model.predict(encoded_tweet)
print("Review: ")
print(decode(encoded_tweet[0]))
print("Prediction: " + str(predict[0]))
