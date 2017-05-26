import urllib.request, urllib.error
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from re import search

domain_regex_front = 'https://exponea.com'
base_url = 'https://exponea.com'
urls = [base_url]
checked_urls = []
images = []

validate = URLValidator()


def process_url(url: str, validate: URLValidator) -> []:

    print('Processing url: %s' % url)


    try:
        validate(url)
    except ValidationError:
        print('Incorrect URL')
        return [], []

    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
    except urllib.error.HTTPError:
        print('HTTP request denied')
        return [], []

    bfsoup = BeautifulSoup(html, 'html.parser')

    fetched_urls = [link['href'] for link in bfsoup.find_all('a', href=True)]
    fetched_images = [link['src'] for link in bfsoup.find_all('img', src=True)]

    return fetched_urls, fetched_images


while len(urls) > 0:

    actual_url = urls[0]
    checked_urls.append(urls.pop(0))

    new_urls, new_images = process_url(actual_url, validate)

    # TODO: check for duplicities
    urls += [url for url in new_urls if url not in urls]
    images += [image for image in new_images if image not in images]

    pass

print(urls)





