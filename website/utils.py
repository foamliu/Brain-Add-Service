import cv2 as cv
import keras.backend as K
import numpy as np
from keras.models import load_model

import pickle
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing import sequence
from keras.preprocessing.image import (load_img, img_to_array)


def colorize_predict(gray):
    h_in, w_in = 256, 256
    h_out, w_out = h_in // 4, w_in // 4
    epsilon = 1e-6
    T = 0.38

    img_rows, img_cols = gray.shape[:2]

    model_path = 'models/model.06-2.5489.hdf5'
    model = load_model(model_path)

    q_ab = np.load("data/pts_in_hull.npy")
    nb_q = q_ab.shape[0]

    L = gray
    gray = cv.resize(gray, (h_in, w_in), cv.INTER_CUBIC)

    x_test = np.empty((1, h_in, w_in, 1), dtype=np.float32)
    x_test[0, :, :, 0] = gray / 255.

    X_colorized = model.predict(x_test)
    X_colorized = X_colorized.reshape((h_out * w_out, nb_q))

    X_colorized = np.exp(np.log(X_colorized + epsilon) / T)
    X_colorized = X_colorized / np.sum(X_colorized, 1)[:, np.newaxis]

    q_a = q_ab[:, 0].reshape((1, 313))
    q_b = q_ab[:, 1].reshape((1, 313))

    X_a = np.sum(X_colorized * q_a, 1).reshape((h_out, w_out))
    X_b = np.sum(X_colorized * q_b, 1).reshape((h_out, w_out))

    X_a = cv.resize(X_a, (img_cols, img_rows), cv.INTER_CUBIC)
    X_b = cv.resize(X_b, (img_cols, img_rows), cv.INTER_CUBIC)

    X_a = X_a + 128
    X_b = X_b + 128

    out_lab = np.zeros((img_rows, img_cols, 3), dtype=np.int32)
    out_lab[:, :, 0] = L
    out_lab[:, :, 1] = X_a
    out_lab[:, :, 2] = X_b

    out_lab = out_lab.astype(np.uint8)
    out_bgr = cv.cvtColor(out_lab, cv.COLOR_LAB2BGR)

    out_bgr = out_bgr.astype(np.uint8)

    K.clear_session()

    return out_bgr


def caption_predict(filename):
    img_rows, img_cols, img_size = 224, 224, 224
    max_token_length = 40
    start_word = '<start>'
    stop_word = '<end>'

    vocab = pickle.load(open('data/vocab_train.p', 'rb'))
    idx2word = sorted(vocab)
    word2idx = dict(zip(idx2word, range(len(vocab))))

    image_model = ResNet50(include_top=False, weights='imagenet', pooling='avg')
    img = load_img(filename, target_size=(img_rows, img_cols))
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    image_input = np.empty((1, img_rows, img_cols, 3))
    image_input[0] = img_array
    encoding = image_model.predict(image_input)

    image_encoding = np.zeros((1, 2048))
    image_encoding[0] = encoding[0]

    model_path = 'models/model.04-1.3820-min.hdf5'
    model = load_model(model_path)
    # print(model.summary())

    start_words = [start_word]
    while True:
        text_input = [word2idx[i] for i in start_words]
        text_input = sequence.pad_sequences([text_input], maxlen=max_token_length, padding='post')
        preds = model.predict([image_encoding, text_input])
        word_pred = idx2word[np.argmax(preds[0])]
        start_words.append(word_pred)
        if word_pred == stop_word or len(start_word) > max_token_length:
            break

    sentence = ' '.join(start_words[1:-1])

    K.clear_session()
    return sentence
