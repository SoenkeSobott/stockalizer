from tensorflow import keras
from util import word_index, train_data, train_labels, test_data, test_labels
from azure.storage.blob import BlobServiceClient
import json
import os

# This script creates a text classification model based on movie reviews.
# The finished model is then saved and uploaded to an Azure blob storage.

# Preprocessing our data: make all reviews the same length
train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post",
                                                        maxlen=100)
test_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post",
                                                       maxlen=100)


# Define model
model = keras.Sequential()
# Make word vectors and then group these vectors if the words are similar and maps the index to vectors
model.add(keras.layers.Embedding(100000, 16))
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

results = model.evaluate(test_data, test_labels)
print(results)
model.save('../data/models/text_classification.h5')


# Upload model to Azure blob storage
def upload_model(blob_client):
    with open("../data/models/text_classification.h5", "rb") as data:
        blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)


# Download from Azure blob
def download_model(blob_client):
    with open("../data/models/text_classification.h5", "wb") as my_blob:
        download_stream = blob_client.download_blob()
        my_blob.write(download_stream.readall())


# Create connection
blob_service_client = BlobServiceClient.from_connection_string(os.environ[CONNECTION_STRING])
container_client = blob_service_client.get_container_client("models")

# Instantiate two blob clients
blob_client_model = container_client.get_blob_client("SentimentAnalysis")
blob_client_word_index = container_client.get_blob_client("WordIndex")

# Upload modell
upload_model(blob_client_model)

# Upload word index
jsonData = json.dumps(word_index)
blob_client_word_index.upload_blob(jsonData, blob_type="BlockBlob", overwrite=True)


