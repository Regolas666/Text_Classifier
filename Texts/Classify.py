import os
import re
from xml.dom.minidom import parse
import numpy as np
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import matplotlib.pyplot as plt
import pickle
import sqlite3
import sys


#os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

title_list = []
text_list = []
class_list = []


def strings(string):
    string = re.sub(r'[^\w\s]+|[\d]+|км/ч|\b\w{0,2}\b', r' ', string)
    string = re.sub(r'\b\w{0,2}\b', r'', string)
    string = re.sub(r'\b\s+\b', r' ', string.strip())
    return string.lower()


for i in range(500):
    for j in range(2):
        dom = parse(f".//xml_news/{j + 1}_{i + 1}.xml")
        text = dom.getElementsByTagName("text")[0]
        text_tag = dom.getElementsByTagName("tags")[0]
        text_tag_ready = text_tag.childNodes[0].nodeValue
        text_title = dom.getElementsByTagName("tags")[0]
        text_title_ready = text_title.childNodes[0].nodeValue
        text_read = text.childNodes[0].nodeValue
        text_read = re.sub(r'\$[^;]*;', '', text_read)
        text_read = text_read.replace('\n\n\n', ' ').replace('  ', '').replace('\n\n', '')
        text_list.append(text_read[1:-1])
        class_list.append(text_tag_ready)
        title_list.append(text_title_ready)

for j in range(1000):
    text_list[j] = strings(text_list[j])

conn = sqlite3.connect('table_of_news.db')
cur = conn.cursor()  # курсор
cur.execute("CREATE TABLE News (Id INT, Title TEXT, Text_news TEXT, Tag TEXT)")

conn.commit()

with conn:
    for i in range(1000):
        cur.execute(f"INSERT INTO News VALUES({i+1}, '{title_list[i]}', '{text_list[i]}', '{class_list[i]}')")
    conn.commit()


y_train_x = []
y_train = []
for j in range(1000):
    if class_list[j] == 'pc':
        y_train_x.append(0)  # если pc - то 0
    else:
        y_train_x.append(1)  # если кино - то 1
y_test = np.array(y_train_x[900:])
y_train = np.array(y_train_x[:-100])
num_words = 2600  # максимальное число слов, которое будем использовать
max_news_len = 100  # максимальная длина новости

# Создаём токенизатор Keras
tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(text_list[:-100])

sequences = tokenizer.texts_to_sequences(text_list[:-100])

# ограничиваем длину отзывов
x_train = pad_sequences(sequences, maxlen=max_news_len)
x_train = np.array(x_train)

# print(x_train[:5]) # проверка первых пяти текстов с новостями

# переходим к свёрточной нейронной сети

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

# print(model.summary())

# обучение, используем callback для сохранения лучшей версии
model_save_path = 'best_model.h5'
checkpoint_callback = ModelCheckpoint(model_save_path,
                                      monitor='val_accuracy',  # сохраняем только том, случае, если доля улучшилась
                                      save_best_only=True,
                                      verbose=1)
# print(class_list[980:])
history = model.fit(x_train,
                    y_train,
                    epochs=8,  # эпохи обучения
                    batch_size=300,  # размер мини-выборки
                    validation_split=0.1,  # используем 10% для проверочного набора данных
                    callbacks=[checkpoint_callback])
# Построим график обучения
# print(1)
plt.plot(history.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

with open('tokenizer_ver1.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)  # сохраняем токенизатор

# Загружаем модель с лучшей долей правильных ответов на проверочном наборе данных
model.load_weights(model_save_path)
# Загружаем набор данных для тестирования
print("Time for some tests!")

test_sequences = tokenizer.texts_to_sequences(text_list[900:])
x_test = pad_sequences(test_sequences, maxlen=max_news_len)
x_test = np.array(x_test)

model.evaluate(x_test, y_test, verbose=1)
"""
print("Введите тестируемое предложение:" + '\n')

text_test_case = input().split()
sequence = tokenizer.texts_to_sequences([text_test_case])
data = pad_sequences(sequence, maxlen=max_news_len)
result = model.predict(data)
if result > 0.5:
    print('Новость относится к pc')
else:
    print('Новость относится к кино')"""
