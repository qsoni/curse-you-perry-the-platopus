import requests
import os
import argparse

from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def createParser():
    parser = argparse.ArgumentParser(description='Описание что делает программа')
    parser.add_argument('start_id', help='начало диапазона', type=int)
    parser.add_argument('end_id', help='конец диапазона', type=int)
    args = parser.parse_args()
    return args.start_id, args.end_id


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError

def parse_book_page(book_id):
    url = f'https://tululu.org/b{book_id}/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    soup = BeautifulSoup(response.text, 'lxml')
    image = soup.find(class_='bookimage').find('img')['src']
    image_url = urljoin(url, image)
    comm = soup.find_all(class_='texts')
    comm = [comment.find('span').text for comment in comm]
    genres = soup.find('span', class_='d_book').find_all('a')
    book_genre = [genre.text for genre in genres]
    return title.strip(), author.strip(), image_url, comm, book_genre

def download_book(book_id, title):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    filename = sanitize_filename(f'{title}.txt')
    filepath = os.path.join('books', filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(image_url, book_id):
    os.makedirs('images', exist_ok=True)
    url = image_url
    response = requests.get(url)
    response.raise_for_status()
    filename = f'{book_id}.jpg'
    filepath = os.path.join('images', filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_books():
    os.makedirs('books', exist_ok=True)
    start_id, end_id = createParser()
    nums = list(range(start_id, end_id))
    for num in nums:
        try:
            title, author, image_url, comm, book_gener = parse_book_page(num)
            download_image(image_url, num)
            download_book(num, title)
            print(title, author)

        except requests.HTTPError:
            print('произошло перенаправление')



download_books()