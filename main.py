import requests
import os

from pathvalidate import sanitize_filename
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
    return title.strip(), author.strip()


def download_book(book_id, title):
    url = f'https://tululu.org/txt.php?id={book_id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filename(f'{title}.txt')
    filepath = os.path.join('books', filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def download_books():
    os.makedirs('books', exist_ok=True)
    nums = list(range(1,11))
    for num in nums:
        try:
            title, author = parse_book_page(num)

            download_book(num, title)
        except requests.HTTPError:
            print('произошло перенаправление')







download_books()
