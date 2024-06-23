from datetime import datetime
from scrapy import Spider

from pymongo import MongoClient

URI = "XYZ"
client = MongoClient(URI)
db = client.news

EXPRESS_COL = db["Express_News"]
GEO_COL = db["Geo_News"]
BOL_COL = db["Bol News"]

def insert_document(collection, title, time, feature_img, description, category):
    doc = {
        "title": title,
        "time": time,
        "featured_img": feature_img,
        "description": description,
        "category": category
    }

    inserted = collection.insert_one(doc)

    return inserted


class NewsCrawler(Spider):
    name = "news-crawler"
    allowed_domains = ["tribune.com.pk", "geo.tv", "bolnews.com"]
    start_urls = ["https://tribune.com.pk/latest", "https://www.geo.tv/latest-news", "https://www.bolnews.com/latest/"]

    def parse(self, response):
        express_css = "li .row > div:first-child div > a:first-child::attr(href)"

        express_news = response.css(express_css).getall()
        geo_news = response.css(".border-box > a::attr(href)").getall()
        bol_news = response.css(".post-link::attr(href)").getall()
    
        if "tribune.com.pk" in response.url:
            for news in express_news:
                yield response.follow(news, callback=self.parse_expressnews)
        
        if "geo.tv" in response.url:
            for news in geo_news:
                yield response.follow(news, callback=self.parse_geonews)

        if "bolnews.com" in response.url:
            for news in bol_news:
                yield response.follow(news, callback=self.parse_bolnews) 
    
    def parse_expressnews(self, response):
        title = response.css("#main-section h1::text").get()
        time = response.css(".left-authorbox span:nth-child(2)::text").get()
        feature_img = response.css(".featured-image-global img::attr(src)").get()
        description = response.css(".story-text p::text").getall()
        category = ""

        description = self.process_description(description)
        insert_document(EXPRESS_COL, title, time, feature_img, description, category)

        yield {
            "title": title,
            "time": time,
            "feature_img": feature_img,
            "description": description,
            "category": category,
        }

    def parse_bolnews(self, response):
        title = response.css(".row h1::text").get()
        feature_img = response.css(".featuredimg img::attr(src)").get()
        description = response.css("div.changeMe p::text").getall()
        time = " ".join(response.css(".date::text").get().split(" ")[1:4])
        category = ""

        description = self.process_description(description)
        insert_document(BOL_COL, title, time, feature_img, description, category)

        yield {
            "title": title, 
            "feature_img": feature_img,
            "description": description,
            "Category": category,
            "time": time
        }

    def process_description(self, desc):
        new_desc = ""

        for i in range(len(desc)):
            new_desc += desc[i]
        
        return new_desc
    
    def parse_geonews(self, response):
        title = response.css("div.story-area h1::text").get()
        time = response.css(".post-time::text").get()
        feature_img = response.css("div.story-area .ui-sortable img::attr(src)").get()
        description = response.css("div.story-area .content-area p::text").getall()
        category = response.css("div.column-right a::attr(title)").get()

        description = self.process_description(description)
        insert_document(GEO_COL, title, time, feature_img, description, category)

        yield {
            "title": title,
            "time": time.replace("\n", ""),
            "feature_img": feature_img,
            "description": description,
            "category": category,
        }
