#!/usr/bin/python

# load modules
from keras.datasets import cifar10
from keras.models import Model, Sequential
from keras.layers import Activation, Dense, Dropout, Flatten, Input
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.optimizers import SGD

# load data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Shape of arrays
print "Shape of X_train:", X_train.shape
print "Shape of X_train:", X_test.shape
print "Shape of y_train:", y_train.shape
print "Shape of y_test:", y_test.shape

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255.0
X_test /= 255.0

# one hot encode the outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

# set up convolutional neural net
data_inputs = Input(shape=(32,32,3))
pipe = Convolution2D(8,3,3, border_mode='same', activation='relu')(data_inputs)
pipe = Convolution2D(8,3,3, border_mode='same', activation='relu')(pipe)
pipe = MaxPooling2D(pool_size=(2, 2))(pipe)
pipe = Dropout(0.25)(pipe)
pipe = Convolution2D(16,3,3, border_mode='same', activation='relu')(pipe)
pipe = Convolution2D(16,3,3, border_mode='same', activation='relu')(pipe)
pipe = MaxPooling2D(pool_size=(2, 2))(pipe)
pipe = Dropout(0.25)(pipe)
pipe = Flatten()(pipe)
pipe = Dense(256, activation='relu')(pipe)
pipe = Dropout(0.5)(pipe)
data_outputs = Dense(10, activation='softmax')(pipe)

# compile and fit the model
my_model = Model(input=data_inputs, output=data_outputs)
my_model.compile(loss='categorical_crossentropy', optimizer='sgd',
                 metrics=['accuracy'])
my_model.fit(X_train, y_train, validation_data=(X_test, y_test),
             batch_size=32, nb_epoch=20)

# Keras example model summary and results
print my_model.summary()

scores = my_model.evaluate(X_test, y_test, verbose=0)
print "Loss: ", (scores[0])
print ("Test Accuracy: %.2f%%" % (scores[1]*100))