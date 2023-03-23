import os
import re

from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pickle


class MainClassify:
    def choose_class(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        num_words = 2600
        max_news_len = 100

        with open('main/tokenizer_ver1.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        model = Sequential()
        model.add(Embedding(num_words, 64, input_length=max_news_len))
        model.add(Conv1D(250, 5, padding='valid', activation='relu'))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        model_save_path = 'main/best_model.h5'
        model.load_weights(model_save_path)
        self = re.sub(r'[^\w\s]+|[\d]+|км/ч|\b\w{0,2}\b', r' ', self)
        self = re.sub(r'\b\w{0,2}\b', r'', self)
        self = re.sub(r'\b\s+\b', r' ', self.strip())
        self = self.lower()
        sequence = tokenizer.texts_to_sequences([self])
        data = pad_sequences(sequence, maxlen=max_news_len)
        result = model.predict(data)
        if result < 0.5:
            return ("Новость относится к pc")
        else:
            return ("Новость относится к кино")
