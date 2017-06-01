from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib
from urllib import request, error
from re import search
from bs4 import BeautifulSoup
from FileHandler import DownloadHandle


class ImageCrawler:
    """
    Crawls images from given url
    Stays within specified domains
    Images are saved into working directory, under subfolder specified in property file
    """

    _url_validator = URLValidator()

    def crawl_images(self, start_url, permitted_domains, dir_save, log):

        urls = [start_url]
        checked_urls = []
        images = []
        dl_handle = DownloadHandle()

        while urls:
            new_urls, new_images = self._crawl_url(urls[0], permitted_domains, log)
            checked_urls.append(urls.pop(0))

            urls = list(set(urls + [url for url in new_urls if url not in checked_urls]))
            images = list(set(images + new_images))

        for url in images:
            dl_handle.download_image(url, dir_save, log)

        log.info('Crawling images finished')

    def _crawl_url(self, url: str, permitted_domains: [], log):

        html_content = self._get_content(url, permitted_domains, log)

        if not html_content:
            return [], []

        soup = BeautifulSoup(html_content, 'html.parser')

        fetched_urls = [link['href'] for link in soup.find_all('a', href=True)]
        fetched_images = [link['src'] for link in soup.find_all('img', src=True)]

        return fetched_urls, fetched_images

    def _url_verify(self, url, permitted_domains, log):

        try:
            ImageCrawler._url_validator(url)
        except ValidationError:
            log.error('Incorrect format of URL: %s' % url)
            return False

        return self._target_domain_verify(url, permitted_domains, log)

    def _get_content(self, url, permitted_domains, log):

        if not self._url_verify(url, permitted_domains, log):
            return None

        try:
            with urllib.request.urlopen(url) as response:
                if bool(search('.*html.*', response.getheader('Content-Type'))):
                    return response.read()

        except urllib.error.HTTPError:
            log.error('HTTP request denied at URL %s' % url)
            return None

        return None

    def _target_domain_verify(self, url, permitted_domains, log):

        if any([bool(search('^'+domain, url)) for domain in permitted_domains]):
            return True
        else:
            log.info('No match for permitted domains at URL: %s' % url)
            return False
