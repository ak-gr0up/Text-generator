# -*- coding: utf-8 -*-
import sys
import argparse
import re
import pickle
import random


class Model:
    def __init__(self, n):
        self.n = n
        self.d = dict()

    def fit(self, prefix, word):
        if self.d.get(prefix) is None:
            self.d[prefix] = list()
        self.d[prefix].append(word)

    def generate(self, prefix):
        if type(prefix) != tuple:
            prefix = tuple(prefix)
        while True:
            cur = self.d.get(prefix)
            if cur is not None:
                return random.choice(cur)
            prefix = prefix[1:]


if __name__ == "__main__":
    desc = """
    По умолчанию:
    Модель сохраняется в model.pkl;
    Текст считывается из stdin в одну строчку;
    n = 2
    """

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input-dir', type=str, help='Путь к файлу с текстом')
    parser.add_argument('--model', type=str, help='Путь куда сохранить модель', default="model.pkl")
    parser.add_argument('--n', type=int, help='Максимальная длина префикса', default=2)

    args = parser.parse_args()

    model_path = args.model
    n = args.n
    text = str()

    if args.input_dir:
        lines = open(args.input_dir, 'r', encoding="utf-8").readlines()
        for l in lines:
            text += l
    else:
        text = input()

    words = re.split('\n| ', text)
    regex = re.compile('[^а-я]')
    raw = [regex.sub('', item.lower().strip()) for item in words]
    data = [item for item in raw if len(item) > 0]

    model = Model(n)

    for right in range(len(data) - 1):
        for left in range(max(right - n + 1, 0), right + 2):
            prefix = tuple(data[left:right + 1])
            model.fit(prefix, data[right + 1])

    pickle.dump(model, open(model_path, 'wb'))
