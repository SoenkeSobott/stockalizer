import tensorflow as tf
from tensorflow import keras
from util import word_index, test_data, test_labels

# This script uses the in 'model.pa' defined model to analyze tweets.

# Get the reverse word index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])


def decode_review(encoded_tweet):
    """Decodes the passed array.

        :param encoded_tweet: encoded tweet array
        :returns: decoded String of the encoded tweet
    """
    return " ".join([reverse_word_index.get(i, "?") for i in encoded_tweet])


def encode_review(tweet_array):
    """Encodes the passed array.

    :param tweet_array: an array of words representing a tweet
    :returns: a array with the mapped values
    """
    encoded = [1]
    for word in tweet:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


# Load the model
model = tf.keras.models.load_model('text_classification')

# TODO: Get tweet
tweet = 'This is a wonderful day. The weather is great and I have a lot of fun here.'
tweet = tweet.replace(".", "").replace(",", "").replace(":", "").split()
encoded_tweet = encode_review(tweet)
encoded_tweet = keras.preprocessing.sequence.pad_sequences([encoded_tweet], value=word_index["<PAD>"], padding="post",
                                                           maxlen=250)

# Predict the value and print to standard output
predict = model.predict(encoded_tweet)
print("Review: ")
print(decode_review(encoded_tweet[0]))
print("Prediction: " + str(predict[0]))
