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

        num_words = 2600  # максимальное число слов, которое будем использовать
        max_news_len = 100  # максимальная длина новости

        with open('main/tokenizer_ver1.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        model = Sequential()
        model.add(Embedding(num_words, 64, input_length=max_news_len))  # создание плотных векторов (64 числа на вектор)
        model.add(Conv1D(250, 5, padding='valid', activation='relu'))  # свёрточная часть (1 свёрточный слой)
        model.add(GlobalMaxPooling1D())  # выбор макс. значений из набора поступающих данных
        model.add(Dense(128, activation='relu'))  # полносвязная часть для классификации
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))  # выходной нейрон

        model.compile(optimizer='adam',  # оптимизатор
                      loss='binary_crossentropy',  # функция ошибки (бинарная перекрёстная энтропия)
                      metrics=['accuracy'])  # доля правильных ответов

        model_save_path = 'main/best_model.h5'
        # Загружаем модель с лучшей долей правильных ответов на проверочном наборе данных
        model.load_weights(model_save_path)

        text_test_case = self
        #  text_test_case = strings(text_test_case)
        self = re.sub(r'[^\w\s]+|[\d]+|км/ч|\b\w{0,2}\b', r' ', self)
        #  string = re.sub(r'http\S+', '', string)  # ????
        self = re.sub(r'\b\w{0,2}\b', r'', self)
        self = re.sub(r'\b\s+\b', r' ', self.strip())
        self = self.lower()
        sequence = tokenizer.texts_to_sequences([text_test_case])
        data = pad_sequences(sequence, maxlen=max_news_len)
        result = model.predict(data)
        if result < 0.5:
            return ("Новость относится к pc")
        else:
            return ("Новость относится к кино")
