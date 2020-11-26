from tensorflow import keras
from util import word_index, train_data, train_labels

# This creates a text classification model based on movie reviews. At the end of the script the model
# is saved and can then be used in other scripts and for other use cases (e.g. tweets).
# See also: https://www.youtube.com/watch?v=k-_pWoy2fb4

# Preprocessing our data: make all reviews the same length
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post",
                                                        maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post",
                                                       maxlen=250)

# Define model
model = keras.Sequential()
# Make word vectors and then group these vectors if the words are similar and maps the index to vectors
model.add(keras.layers.Embedding(10000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation="relu"))
model.add(keras.layers.Dense(1, activation="sigmoid"))  # sigmoid: output numbers are between 0 and 1

model.summary()
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

x_val = train_data[:100000]
x_train = train_data[10000:]

y_val = train_labels[:100000]
y_train = train_labels[10000:]

fit_model = model.fit(x_train, y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

model.save('text_classification')
