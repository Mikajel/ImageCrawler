import urllib.request, urllib.error
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

base_url = 'http://exponea.com'
urls = [base_url]
checked_urls = []
images = []


def process_url(url: str) -> []:

    print('Processing url: %s' % url)

    validate = URLValidator()
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

    new_urls, new_images = process_url(actual_url)

    # TODO: check for duplicities
    urls += new_urls
    images += new_images

    pass

print(urls)





