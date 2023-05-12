import requests
import os

from pathvalidate import sanitize_filename
from urllib.parse import urljoin
from bs4 import BeautifulSoup


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
    return title.strip(), author.strip(), image_url


def download_book(book_id, title):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    filename = sanitize_filename(f'{title}.txt')
    filepath = os.path.join('books', filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_image(image_url, book_id):
    url = image_url
    response = requests.get(url)
    response.raise_for_status()
    filename = f'{book_id}.jpg'
    filepath = os.path.join('images', filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_books():
    os.makedirs('books', exist_ok=True)
    nums = list(range(1,11))
    for num in nums:
        try:
            title, author, image_url = parse_book_page(num)
            download_image(image_url, num)
            download_book(num, title)
        except requests.HTTPError:
            print('произошло перенаправление')
download_books()