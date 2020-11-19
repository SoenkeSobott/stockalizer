import tensorflow as tf
from text_classification_model import word_index, test_data, test_labels

# Get the reverse word index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# Function to decode/map the index to a word
def decode_review(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])


# Get model
model = tf.keras.models.load_model('text_classification')

index = 29
test_review = test_data[index]
predict = model.predict([test_review])
print("Review: ")
print(decode_review(test_review))
print("Prediction: " + str(predict[0]))
print("Actual: " + str(test_labels[index]))
