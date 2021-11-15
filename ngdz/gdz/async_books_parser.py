import json
from bs4 import BeautifulSoup
import requests
import time
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}

dict_lessons = {}
list_links = []
start_time = time.time()
books_data = []
list_lessons = []
list_klasses = []


def get_links():
    print('[INFO] Получение ссылок')
    response = requests.get('https://gdz.ru').text
    soup = BeautifulSoup(response, 'lxml')

    lessons = soup.find_all('tr', class_='main-table-row')

    for lesson in lessons:
        dict_lessons[lesson.td.a['href'].split('/')[1]] = lesson.td.a.text.strip()
        for cat_link in lesson.find_all('td', class_=''):
            a = cat_link.a
            if a.has_attr('class'):
                continue
            link = 'https://gdz.ru' + a['href']
            list_links.append(link)


def map_lessons(book):
    return book['lesson']


def map_classes(book):
    kl = {
        'klass': int(book['klass']),
        'lesson': book['lesson'],
    }
    return kl


def save_lessons():
    global list_lessons, list_klasses
    list_lessons = list(set(map(map_lessons, books_data)))
    list_lessons.sort()
    list_klasses = list(map(map_classes, books_data))
    list_klasses = [dict(t) for t in {tuple(d.items()) for d in list_klasses}]
    list_klasses = list(sorted(list_klasses, key=lambda item: item['klass']))


async def get_page_data(session, url):
    klass = url.split('/')[-3].split('-')[1]
    lesson = url.split('/')[-2]

    async with session.get(url=url, headers=headers) as response:
        response_text = await (response.text())
        soup = BeautifulSoup(response_text, 'lxml')

        books = soup.find_all('li', class_='book')

        for b in books:
            if len(b.find_all('p', class_='book-description_premium')):
                continue
            l_title = dict_lessons[lesson]
            title = ' '.join(b.find('p', class_='book-description-main').text.split())
            author = ' '.join(b.find('span', itemprop='author').text.split())
            img = 'https:' + b.find('img')['data-src']
            link = 'https://gdz.ru' + b.a['href']
            slug = link.split('/')[-2]
            url = f'/{lesson}/{klass}/{slug}/'
            books_data.append({'lesson': l_title, 'l_slug': lesson, 'klass': klass, 'title': title, 'slug': slug, 'author': author, 'img': img, 'link': link, 'url': url})

    # print(f'[INFO] Обработал страницу {page}')


async def gather_data():
    print('[INFO] Отработка страниц')
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(len(list_links)):
            task = asyncio.create_task(get_page_data(session, list_links[page]))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main_books_parser():
    get_links()

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(gather_data())

    save_lessons()

    print('[INFO] Сохранение данных')

    with open('data/books_data_async.json', 'w') as f:
        json.dump(books_data, f)

    with open('data/lessons_data_async.json', 'w') as f:
        json.dump(list_lessons, f)

    with open('data/klasses_data_async.json', 'w') as f:
        json.dump(list_klasses, f)

    print(f'[INFO] Получено {len(books_data)} книг')
    print(f'[INFO] Затраченное время: {time.time() - start_time}')


if __name__ == '__main__':
    main_books_parser()
