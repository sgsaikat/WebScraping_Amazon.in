# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonItem

class AmazonspiderSpider(scrapy.Spider):
    name = 'amazonspider'
    start_urls = [
        'https://www.amazon.in/b?node=12440869031&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-5&pf_rd_r=TYJ58DS4A4B85ZHK91JS&pf_rd_t=101&pf_rd_p=87ca2a2c-7a96-4ae0-93e7-689c0a32d457&pf_rd_i=1634753031'
        ]
    page_number = 2

    def parse(self, response):
        self.logger.info(f'Parse function called on {response.url}')
        items = AmazonItem()

        page_title = response.css('title::text').extract_first()
        item_rows = response.css('.s-result-item')
        
        for row in item_rows:
            try:
                book_title = row.css('.s-access-title::text').extract_first()
                if not book_title:
                    book_title = row.css('.a-color-base.a-text-normal::text').extract_first()

                book_author = row.css('.a-color-secondary+ .a-color-secondary').css('::text').extract_first()
                if not book_author:
                    book_author = row.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract_first().strip()
                
                prices = row.css('.a-color-secondary+ .a-text-bold').css('::text').extract()
                if not prices:
                    book_price = row.css('.a-price span').css('::text').extract_first()[1:]
                else:
                    for price in prices:
                        try:
                            book_price = float(price)
                        except ValueError:
                            pass

                book_image_link = row.css('.cfMarker::attr(src)').extract_first()
                if not book_image_link:
                    book_image_link = row.css('.s-image::attr(src)').extract_first()

                book_detail_link = row.css('.s-access-detail-page::attr(href)').extract_first()
                if not book_detail_link:
                    book_detail_link = 'https://www.amazon.in' + row.css('.a-link-normal.a-text-normal::attr(href)').extract_first()

                items['page_title'] = page_title
                items['book_title'] = book_title
                items['book_author'] = book_author
                items['book_price'] = book_price
                items['book_image_link'] = book_image_link
                items['book_detail_link'] = book_detail_link
                
                yield items
            except Exception as err:
                print(err)

        # next_page = response.css('a.pagnNext::attr(href)').extract_first()
        next_page = f'https://www.amazon.in/s?i=digital-text&rh=n%3A12440869031&page={AmazonspiderSpider.page_number}&qid=1576272599&ref=sr_pg_{AmazonspiderSpider.page_number}'
        if AmazonspiderSpider.page_number <= 7:
            print("="*30, AmazonspiderSpider.page_number)
            AmazonspiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
