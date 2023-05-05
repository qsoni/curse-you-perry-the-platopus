import requests
import os


from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()


soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
#print(title_tag)
title_text = title_tag.text
#print(title_text)
#print(soup.find('img', class_='attachment-post-image')['src'])
print(soup.find('main').find(class_='entry-content').text)