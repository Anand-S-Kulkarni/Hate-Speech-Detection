# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 20:05:11 2020

@author: Madhuri
"""

import pickle
from custom import Custom
import numpy as np
import pandas as pd
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, SpatialDropout1D
from keras.layers.embeddings import Embedding

class ModelGlove():
    
  DATADIR = 'C:/Users/Madhuri/Desktop/HateSpeech/dataset/dataset.csv'
  df = pd.read_csv(DATADIR)
  labels = df['label']
  
  def read_data(self):
      self.df.dropna()
      self.df = self.df.select_dtypes(include=['object']).copy()
      self.df[self.df.isnull().any(axis=1)]
      cleanup_nums = {"label":{"noHate": 0, "hate": 1}}
      self.df.replace(cleanup_nums, inplace=True)  
    
  def clean_tweet(self,x):
      x = x.lower()
      x = re.sub('@[A-Za-z0-9]+', "", x)
      x = re.sub('#[A-Za-z0-9]+', "", x)
      x = re.sub('[0-9]+', "", x)
      x = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', "", x)
      x = re.sub('www.[a-z0-9]*.com', "", x)
      x = re.sub(r"\'ve", " have ", x)
      x = re.sub(r"n't", " not ", x)
      x = re.sub(r"i'm", "i am ", x)
      x = re.sub(r"\'re", " are ", x)
      x = re.sub(r"not", " noti ", x)
      x = re.sub("\W+", " ", x)
      x = re.sub(r"noti", " not ", x)
      x = re.sub("\s+", " ", x)
      preprocessed_tweet = ' '.join([w for w in x.split() if len(w)>2])
      return preprocessed_tweet  

  def preprocess(self):
      self.df['tweet'] = self.df['tweet'].map(lambda x : self.clean_tweet(x))  

  def build_model(self):
      tokenizer = Tokenizer(num_words=20000)
      tokenizer.fit_on_texts(self.df['tweet'])
      sequences = tokenizer.texts_to_sequences(self.df['tweet'])
      data = pad_sequences(sequences, maxlen=100)
      vocabulary_size = len(tokenizer.word_index)+1
      
      x_train, x_test, y_train, y_test = train_test_split(data, self.labels, test_size=0.20, random_state=42)
      
      embeddings_index = dict()
      
      with open('C:/Users/Madhuri/Desktop/HateSpeech/dataset/glove.6B.100d.txt', encoding='utf8') as f:
          for line in f:
              values = line.split()
              word = values[0]
              coefs = np.asarray(values[1:], dtype='float32')
              embeddings_index[word] = coefs
      f.close()
      
      embedding_matrix = np.zeros((vocabulary_size, 100))
      
      for word, index in tokenizer.word_index.items():
          if index > vocabulary_size - 1:
              break
          else:
              embedding_vector = embeddings_index.get(word)
              if embedding_vector is not None:
                  embedding_matrix[index] = embedding_vector
      
      model_glove = Sequential() 
      model_glove.add(Embedding(vocabulary_size, 100, input_length=100, weights=[embedding_matrix], trainable=True))
      model_glove.add(SpatialDropout1D(0.25))
      model_glove.add(Conv1D(128, 5, activation='relu'))
      model_glove.add(MaxPooling1D(pool_size=4))
      model_glove.add(LSTM(128, dropout=0.1))
      model_glove.add(Dense(2, activation='softmax'))
      model_glove.compile(loss='sparse_categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-3), metrics=['accuracy'])
      model_glove.fit(x_train, y_train, validation_split=0.20, epochs=5, batch_size=128)

  def model(self):
      wrap = Custom()
      return wrap
      
serializable_obj = ModelGlove()
obj = serializable_obj.model()
saved_model = "C:/Users/Madhuri/Desktop/HateSpeech/dataset/Model.pkl" 
with open(saved_model, 'wb') as file:  
    pickle.dump(obj, file)