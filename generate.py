# -*- coding: utf-8 -*-
from train import Model
import argparse
import pickle

desc = """
По умолчанию:
Начало последовательности генерирует модель;
Путь к сохраненной модели model.pkl
"""

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('--prefix', type=str, help='Начало последовательности слов', default="")
parser.add_argument('--model', type=str, help='Путь к сохраненной модель', default="model.pkl")
parser.add_argument('--length', type=int, required=False, help='Длина генерируемой последовательности')

args = parser.parse_args()

model_path = args.model
length = args.length
prefix = args.prefix

model = pickle.load(open(model_path, 'rb'))

n = model.n
res = prefix.split()

for i in range(length):
    res.append(model.generate(res[-n:]))

print(*res)
