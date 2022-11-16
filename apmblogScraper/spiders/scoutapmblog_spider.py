import scrapy
from ..items import ApmblogscraperItem

class apmblogspider(scrapy.Spider):
    name = 'scoutapmblog'
    start_urls =  [
        'https://scoutapm.com/blog/categories/engineering',
        'https://scoutapm.com/blog/categories/performance',
        ]

    def parse(self, response):
        blogs = response.css('.post-partial')
        for blog in blogs:
            blog_link = blog.css('a::attr(href)').get()
            yield response.follow(blog_link, callback = self.detail_page)

        next_page = response.css('.glyphicon-menu-right::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback = self.parse)

    def detail_page(self, response):
        items = ApmblogscraperItem()

        title = response.css('.single-post h1::text').get()
        author = response.css('.author-link::text').get()
        author_link = response.css('.author-link::attr(href)').get()
        author_link = 'https://scoutapm.com' + author_link
        date = response.css('.post-meta::text').getall()[-1].strip().replace('on\n      ', '')
        category = response.css('.post-tags a::text').get()

        items['title'] = title
        items['author'] = author
        items['author_link'] = author_link
        items['date'] = date
        items['category'] = category

        yield items