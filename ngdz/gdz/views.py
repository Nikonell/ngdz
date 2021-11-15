import time
from multiprocessing import Process, context
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import render
from .read_json_data import read_books, read_lessons, read_klasses
from .async_books_parser import main_books_parser
from .book_tasks import main_tasks_parser
from .task_imgs import main_img_parser

lastparse = time.time()

def auto_parse():
    global lastparse
    if time.time() > lastparse + 86400000:
        process = Process(target=main_books_parser)
        process.start()
        lastparse = time.time()


def index(request):
    auto_parse()

    lessons = read_lessons()
    klasses = read_klasses()
    books = read_books()

    context = {
        'title': 'Главная страница',
        'lessons': lessons,
        'klasses': klasses,
        'books': books,
    }

    return render(request, 'gdz/index.html', context)


def show_book(request, lesson, klass, book_slug):
    books = read_books()
    book = list(filter(lambda b: b['l_slug'] == lesson and b['klass'] == str(klass) and b['slug'] == book_slug, books))[0]
    task_list = main_tasks_parser(book['link'])
    context = {
        'book': book,
        'task_list': task_list,
    }
    return render(request, 'gdz/book.html', context=context)


def show_task(request, task_link):
    link_split = task_link.split('/')
    b_lesson = link_split[1]
    b_klass = link_split[0].split('-')[1]
    b_slug = link_split[2]

    books = read_books()
    book = list(filter(lambda b: b['l_slug'] == b_lesson  and b['klass'] == b_klass and b['slug'] == b_slug, books))[0]

    imgs = main_img_parser('https://gdz.ru/' + task_link)
    if not len(imgs):
        raise Http404()

    context = {
        'book': book,
        'imgs': imgs,
    }
    
    return render(request, 'gdz/task.html', context=context)


def manual_parse(request):
    global lastparse
    process = Process(target=main_books_parser)
    process.start()
    lastparse = time.time()
    return HttpResponse('Парсинг запущен')
