# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Scraped data -> Item Containers -> JSON/CSV files
# Scraped data -> Item Containers -> Pipeline -> SQL/Mongo DB

import sqlite3

class AmazonPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('short_reads.db')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("DROP TABLE IF EXISTS books_tb")
        self.curr.execute("""CREATE TABLE books_tb
                            (
                                page_title text,
                                book_title text,
                                book_author text,
                                book_price float,
                                book_image_link text,
                                book_detail_link text
                            )
                        """)

    def store_db(self, item):
        self.curr.execute("INSERT INTO books_tb VALUES (?, ?, ?, ?, ?, ?)",
                            (item['page_title'], 
                            item['book_title'],
                            item['book_author'],
                            item['book_price'],
                            item['book_image_link'],
                            item['book_detail_link']
                            )
                        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def __del__(self):
        self.conn.close()
