import traceback
import uuid
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
from urllib.request import urlopen
from enum import Enum


### CSS SELECTOR EXAMPLE
# yield {
#                 'text': content.css(TEXT_SELECTOR).getall(),
#             }

output_dir_path = "D:\\Datasets\\Texts\\Seinfeld scripts\\"
output_file_name = output_dir_path + str(uuid.uuid4()) + ".txt"
exchangeable_xpath_link_selector = '//p/a/@href'
exchangeable_css_content_selector = '//p/a/@href'
exchangeable_allowed_domains = ['example.com']
exchangeable_start_urls = ['example.com']
selected_spider = "FILEDOWNLOAD"

def download_files(url):

    file_name = output_dir_path
    file_name += url.split('/')[-1]
    opened_url = urlopen(url)
    opened_file = open(file_name, 'wb')
    file_size = int(opened_url.getheader("Content-Length"))
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = opened_url.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        opened_file.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print(status)

    opened_file.close()


class FileDownloadSpider(scrapy.Spider):
    name = "file_download_spider"
    start_urls = exchangeable_start_urls
    allowed_domains = exchangeable_allowed_domains

    def parse(self, response):

        base_url = response.url

        try:
            download_files(base_url, "pdf")
        except:
            print(traceback.format_exc())
            return

        links = response.xpath(exchangeable_xpath_link_selector).getall()
        for link in links:
            yield Request(
                urljoin(base_url, link),
                callback=self.parse
            )


class TextDownloadSpider(scrapy.Spider):
    name = "text_download_spider"
    start_urls = exchangeable_start_urls
    allowed_domains = exchangeable_allowed_domains

    def parse(self, response):

        base_url = response.url
        CONTENT_SELECTOR = '#content'
        for content in response.css(CONTENT_SELECTOR):
            TEXT_SELECTOR = 'p ::text'
            with open(output_file_name, "a", encoding="utf8") as f:
                for text in content.css(TEXT_SELECTOR).getall():
                    f.write(text)

        NEXT_PAGE_SELECTOR = '//td/a/@href'
        links = response.xpath(NEXT_PAGE_SELECTOR).getall()
        for link in links:
            yield Request(
                urljoin(base_url, link),
                callback=self.parse
            )


def spider_chooser(spider_str):
    return {
        "FILEDOWNLOAD": FileDownloadSpider,
        "TEXTDOWNLOAD": TextDownloadSpider
    }.get(spider_str, None)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    })

    spider_choices = {"FILEDOWNLOAD": FileDownloadSpider,
        "TEXTDOWNLOAD": TextDownloadSpider}

    process.crawl(spider_choices.get(selected_spider, None))
    process.start()
    print("Crawl finished, exiting...")
