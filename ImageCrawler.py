import urllib.request
from bs4 import BeautifulSoup

base_url = 'http://exponea.com'
urls = [base_url]
checked_urls = []
images = []


def process_url(url: str) -> []:

    print('Processing url: %s' % url)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        bfsoup = BeautifulSoup(html, 'html.parser')

        new_urls = [link['href'] for link in bfsoup.find_all('a', href=True)]
        new_images = [link['src'] for link in bfsoup.find_all('img', src=True)]

        return new_urls, new_images


def get_all_urls(a_refs: []) -> []:

    urls = []

    for link in a_refs:
        urls.append(link.get('href'))

    return urls


# Extracts image URLs from a list of <img> HTML tags
# Returns a list of URL strings
# Example:
#   [<img src="https://exponea.com/randomimage.png" class="platform-overview__image"/>]
#       -> [https://exponea.com/randomimage.png]
def get_all_images(img_refs: []) -> []:

    urls = []

    for link in img_refs:
        urls.append(link.get('src'))

    return urls


while len(urls) > 0:

    actual_url = urls[0]
    checked_urls.append(urls.pop(0))

    new_urls, new_images = process_url(actual_url)

    # TODO: check for duplicities
    urls += new_urls
    images += new_images

    pass

print(urls)





