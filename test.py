import requests


from bs4 import BeautifulSoup

def parse_book_page():
    url = 'https://tululu.org/b5/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title, author = soup.find('h1').text.split('::')
    img = soup.find(class_='bookimage').find('img')['src']
    print(img)

parse_book_page()