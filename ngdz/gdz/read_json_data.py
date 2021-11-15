import json


def read_lessons():
    with open('data/lessons_data_async.json', 'r') as f:
        return json.load(f)


def read_klasses():
    with open('data/klasses_data_async.json', 'r') as f:
        return json.load(f)


def read_books():
    with open('data/books_data_async.json', 'r') as f:
        return json.load(f)
