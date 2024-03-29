# -*- coding: utf-8 -*-
"""IMDb Sentimental analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CDesYNzdhT90YriCA5Ad7kf0lEWv2y4o
"""

!pip install tensorflow==1.14.0
import tensorflow as tf
print(tf.__version__)

# LSTM and CNN for sequence classification in the IMDB dataset
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import numpy as np
import os
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing import sequence
os.environ['COLAB_SKIP_TPU_AUTH'] = '1'
import tensorflow.compat.v2 as tf
import tensorflow_datasets as tfds

# tfds works in both Eager and Graph modes
#tf.enable_v2_behavior()
import tokenize
from tensorflow import keras

# fix random seed for reproducibility
from tensorflow.keras import backend
np.random.seed(7)

np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)

dataset, information = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
train_dataset, test_dataset = dataset['train'], dataset['test']

# load the dataset but only keep the top n words, zero the rest
imdb = keras.datasets.imdb
top_words=5000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=top_words)
print(X_train[0])
word_to_id = keras.datasets.imdb.get_word_index()
id_to_word = {value:key for key,value in word_to_id.items()}
for id in X_train[0]:
  print("********************************************")
  print(id)
  print(' '.join(id_to_word.get(id - 3, '?')))

# restore np.load for future normal usage
np.load = np_load_old

# truncate and pad input sequences
max_review_length = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
model.add(Conv1D(filters=64, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(Dropout(0.25))
model.add(LSTM(70))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train,validation_data=(X_test, y_test), epochs=3, batch_size=64)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

import keras
from keras.preprocessing.text import Tokenizer
def conv_to_proper_format(sentence):
  word_index=imdb.get_word_index()
  #msentence=Tokenizer(num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ', char_level=False, oov_token=None, document_count=0)
  print(sentence)
  sentence=np.array([word_index[word] if word in word_index else 0 for word in sentence])#Encoding into sequence of integers
  sentence[sentence>5000]=2
  L=500-len(sentence)
  sentence=np.pad(sentence, (L,0), "constant")
  sentence=sentence.reshape(1,-1)
  print(sentence)
  return sentence

r1=conv_to_proper_format("bad movie")
model.predict(r1)

vec=imdb.get_word_index()
def get_senti(sent):
    m=494
    x=np.zeros((1,500))
    for i in sent.split():
      x[0][m]=(vec[i]+3)
      m=m+1
      #print(x)
    return x

r1=get_senti("this movie could have been better")
model.predict(r1)

import keras
def conv_to_proper_format(sentence):
  word_index=imdb.get_word_index()
  #sentence=keras.preprocessing.text.Tokenizer(num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ',)
  print(sentence)
  sentence=np.array([word_index[word] if word in word_index else 0 for word in sentence])#Encoding into sequence of integers
  #Encoding into sequence of integers
  sentence[sentence>5000]=2
  L=500-len(sentence)
  sentence=np.pad(sentence, (L,0), "constant")
  sentence=sentence.reshape(1,-1)
  print(sentence)
  return sentence

r1=conv_to_proper_format(["this", "was", "a" ,"good" ,"movie"])
model.predict(r1)

from keras.preprocessing.text import Tokenizer
print("Please Enter your valuable review")
gt=input()
#gtg=["good","bad","random"]
gtg=[gt]
tokenizer = Tokenizer(num_words=1000, filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n')
tokenizer.fit_on_texts([gt])
X_tests = tokenizer.texts_to_sequences([gt])
# X_tests = Tokenizer[texts_to_sequences(gtg)]
X_tests = sequence.pad_sequences(X_tests, maxlen=len_max)
y_pred=model.predict_classes(X_tests)
if(y_pred==1):
  y_pred=0
if(y_pred>1):
  y_pred=1
print(gtg)
print(y_pred)

