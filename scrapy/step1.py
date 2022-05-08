# -*- coding: utf-8 -*-
import scrapy


class Link(scrapy.Item):
    link = scrapy.Field()


class LinkListsSpider(scrapy.Spider):
    one_hundred_pages = True  # <-----------------------------------------------------

    name = 'step1'
    allowed_domains = ['https://www.filmweb.pl/persons/']
    list_of_links = []
    # Generating links to pagination pages
    if one_hundred_pages == True:
        paginations = 10  # 10 x 10 = 100 subpages
    else:
        paginations = 1000  # There are 1000 pages in total

    for page in range(1, paginations + 1):
        list_of_links.append(f"https://www.filmweb.pl/persons/search?orderBy=popularity&descending=true&page={page}")

    start_urls = list_of_links

    def parse(self, response):

        xpath = "//h3/a[starts-with(@href, '/person/')]/@href"
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.filmweb.pl' + s.extract()
            yield l
