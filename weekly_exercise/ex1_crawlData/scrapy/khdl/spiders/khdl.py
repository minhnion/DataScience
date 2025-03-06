import scrapy
import re
from scrapy.selector import Selector

class KHDLspider(scrapy.Spider):
    name = "chungkhoan"
    ALLOWED_DOMAINS = ['vnexpress.net']
    start_urls = [
        "https://vnexpress.net/kinh-doanh/chung-khoan"
    ]

    def parse(self, response):
        all_links = response.css("div.width_common.list-news-subfolder.has-border-right > article > div > a::attr(href)").getall()
        yield from response.follow_all(all_links, self.parse_post)

        next_page = response.css("#pagination > div > a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_post(self, response):
        title = response.css("section.section.page-detail.top-detail > div > div.sidebar-1 > h1::text").get()
        if title:
            title = title.strip()
        else:
            title = ""

        description = response.css("section.section.page-detail.top-detail > div > div.sidebar-1 > p::text").get()
        if description:
            description = description.strip()
        else:
            description = ""

        paragraphs = response.css("section.section.page-detail.top-detail > div > div.sidebar-1 > article *::text").getall()
        content = "\n".join([p.strip() for p in paragraphs if p.strip()])


        yield {
            "link": response.url,
            "title": title,
            "description": description,
            "content": content
        }