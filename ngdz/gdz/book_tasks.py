import requests
from bs4 import BeautifulSoup

def map_groups(group):
    if group.h2:
        title = group.h2.text.strip()
    elif group.h3:
        title = group.h3.text.strip()
    else:
        return None
    if group.section:
        return None
    
    list_tasks = group.find_all('a', class_='task-button')
    tasks = list(map(lambda t: {'title': t['title'], 'link': t['href']}, list_tasks))
    return {'title': title, 'tasks': tasks}


def main_tasks_parser(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    }

    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    list_groups = soup.find_all('section', class_='section-task')

    groups = list(filter(lambda b: b != None, map(map_groups, list_groups)))
    return groups
