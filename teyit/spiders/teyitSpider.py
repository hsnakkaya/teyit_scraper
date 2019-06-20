# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import *
import pprint


class TeyitspiderSpider(scrapy.Spider):
    name = 'teyitSpider'
    allowed_domains = ['teyit.org']
    start_urls = ['http://teyit.org/']

    def start_requests(self):
        url_list = ['https://teyit.org/konu/analiz/page/1/',
                    'https://teyit.org/konu/dosya/page/1/',
                    'https://teyit.org/konu/icgoru/page/1/',
                    'https://teyit.org/konu/teyitpedia/page/1/']

        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        raw = response.body
        soup = BeautifulSoup(raw, 'html.parser')

        # get the next page link, if exists.
        next_page = soup.select_one('#cb-blog-infinite-load a')
        if next_page is not None:
            next_page = next_page['href']
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        # scrape article url's
        items = soup.select('.cb-meta.clearfix .cb-post-title a')
        for item in items:
            url = item['href']
            print(url)
            yield scrapy.Request(url=url, callback=self.article_parse)

    def article_parse(self, response):
        article = Article()
        print('\n\n')

        raw = response.body
        soup = BeautifulSoup(raw, 'html.parser')

        url = response.url
        # print(url)

        title = soup.select_one('.cb-entry-title').text.strip()
        # print(title)

        author = soup.select_one('.cb-author a').text.strip()
        # print(author)

        date = soup.select('.cb-meta.clearfix time')[0]['datetime']
        # print(date)

        claim = soup.select_one('.iddia_text')
        verdict = soup.select_one('.iddia_title')

        if claim is not None:
            is_claim = True
            claim = claim.text.strip()
            verdict = verdict.text.strip()
        else:
            is_claim = False
            claim = ''
            verdict = ''

        links = soup.select('.cb-entry-content a , .cb-itemprop a')
        link_list = []
        for link in links:
            # print(item)
            link_url = link['href']
            link_text = link.text.strip()
            link = [link_text, link_url]
            if len(link_text) > 1:
                link_list.append(link)

        # pprint.pprint(link_list)
        # print('\n\n')

        imgs = soup.select('.size-full')
        img_link_list = []
        for img in imgs:
            # print(item)
            img_link_list.append(img['src'])

        # pprint.pprint(img_link_list)
        # print('\n\n')

        text = soup.select('.cb-itemprop~ p , .cb-itemprop span')
        text_all = ''
        for piece in text:
            # print(piece)
            text_all = text_all + ' ' + str(piece.text.strip())

        # pprint.pprint(text_all)
        # print('\n\n')

        tags = soup.select('.cb-tags a')
        tag_list = []
        for tag in tags:
            tag_name = tag.text
            tag_url = tag['href']
            tag = [tag_name, tag_url]
            tag_list.append(tag)
        #     print(tag_name + ' ' + tag_url)
        #         #
        #         # print('\n\n\n\n')

        article['url'] = url
        article['title'] = title
        article['author'] = author
        article['date'] = date
        article['claim'] = claim
        article['verdict'] = verdict
        article['is_claim'] = is_claim
        article['link_list'] = link_list
        article['img_link_list'] = img_link_list
        article['text_all'] = text_all
        article['tags'] = tag_list

        yield article
