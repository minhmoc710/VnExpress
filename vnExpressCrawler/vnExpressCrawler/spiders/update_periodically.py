import scrapy
from ..items import ArticleItem


NEWS_ARTICLE = 'article'


class UpdatePeriodicallySpider(scrapy.Spider):
    name = 'update_periodically'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/tin-tuc-24h/']

    def parse(self, response):
        for link in response.css(".title-news a::attr(href)").getall():
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        website_type = response.css(
            "meta[name='tt_page_type']::attr(content)").get()
        if website_type == NEWS_ARTICLE:
            objectid = response.css(
                "meta[name='tt_article_id']::attr(content)").get()
            article_items = ArticleItem()
            article_items['articleID'] = objectid
            article_items['content'] = " ".join(response.css(
                ".Normal ::text, .description ::text").getall())
            article_items['tags'] = response.css(
                "meta[name='its_tag'] ::attr(content)").extract()[0].split(", ")
            article_items['title'] = response.css(
                "meta[property='og:title']::attr(content)").get()
            article_items['time'] = response.css(
                "meta[name='its_publication'] ::attr(content)").get()
            article_items['link'] = response.url
            article_items['category'] = response.css(
                "meta[name='its_subsection']::attr(content)").get().split(", ")
            article_items['displayContent'] = response.css(".fck_detail").get()
            article_items['sapo'] = response.css(
                "meta[itemprop='description']::attr(content)").get()
            article_items['thumbnail'] = response.css(
                "meta[itemprop='thumbnailUrl']::attr(content)").get()
            yield article_items
