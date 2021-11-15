import requests
from bs4 import BeautifulSoup


def main_img_parser(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    img_containers = soup.find_all('div', class_='task-img-container')

    imgs = list(map(lambda c: 'https:' + c.img['src'], img_containers))
    return imgs
