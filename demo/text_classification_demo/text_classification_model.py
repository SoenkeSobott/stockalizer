from tensorflow import keras

# From here: https://www.youtube.com/watch?v=k-_pWoy2fb4

# Get movie review data from keras
data = keras.datasets.imdb

# Load data with only the words that occur at least 10000 times
(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=10000)

# Get word index of the data and add our own 'helper' words to the list
word_index = data.get_word_index()
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# Preprocessing our data: make all reviews the same length
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post", maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post", maxlen=250)

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