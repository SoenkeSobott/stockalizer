import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

mnist = tf.keras.datasets.mnist # 28X28 images of hand-written digits 0-9

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis=1)
x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=3)

# Calculate loss
val_loss, val_acc = model.evaluate(x_test, y_test)
print('Loss: ', val_loss)
print('Acc: ', val_acc)


model.save('num_prediction')
new_model = tf.keras.models.load_model('num_prediction')

predictions = new_model.predict([x_test])

print(predictions)
print("Predicion: ", np.argmax(predictions[0]))

plt.imshow(x_test[0])
plt.show()