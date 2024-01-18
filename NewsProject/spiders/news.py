from scrapy import Spider


class NewsCrawler(Spider):
    name = "news-crawler"
    allowed_domains = ["tribune.com.pk", "geo.tv", "bolnews.com"]
    start_urls = ["https://tribune.com.pk/latest", "https://www.geo.tv/latest-news", "https://www.bolnews.com/latest/"]

    def parse(self, response):
        express_css = "li .row > div:first-child div > a:first-child::attr(href)"

        express_nextpage = response.css(".pagination li:nth-child(2) > a::attr(href)").get()
        express_links = response.css(express_css).getall()
        geo_links = response.css(".border-box > a::attr(href)").getall()
        bol_links = response.css(".post-link::attr(href)").getall()
    
        # if "tribune.com.pk" in response.url:
        #     for link in express_links:
        #         yield response.follow(link, callback=self.parse_express_news)
        
        #     if express_nextpage:
        #         yield response.follow(express_nextpage, callback=self.parse)
        
        # if "geo.tv" in response.url:
        #     for link in geo_links:
        #         yield response.follow(link, callback=self.parse_geo_news)

        if "bolnews.com" in response.url:
            for link in bol_links:
                yield response.follow(link, callback=self.parse_bol_news)
        
        
    
    def parse_express_news(self, response):
        headline_css = ".mainstorycontent-parent .story-text > p:nth-child(2)::text"
    
        title = response.css("#main-section h1::text").get()
        headline = response.css(headline_css).get()
        time = response.css(".left-authorbox span:nth-child(2)::text").get()
        author = response.css(".left-authorbox a::text").get()
        feature_img = response.css(".featured-image-global img::attr(src)").get()
        description = self.description(response)
        category = "helo"
        url = response.url


        yield {
            "title": title,
            "headline": headline,
            "time": time,
            "author": author,
            "feature_img": feature_img,
            "description": description,
            "category": category,
            "URL": url,
        }

    def description(self, response):
        description = response.css(".story-text p span::text").getall()
        new_description = ""
        
        for i in range(len(description)-7):
            new_description += description[i]
        
        return new_description


    # def parse_sama_data(self, response):
    #     title = response.css("#content h1::text").get()
    #     headline = response.css("p > strong::text").get()
    #     time = response.css("#content time::text").get()
    #     author = response.css("#content article strong > a::text")
    #     feature_img = response.css(".img-frame img::attr(src)").get()
    #     description = response.css("#content p::text").get
    #     category = self.sama_category(response)
    #     url = response.url

    #     yield {
    #         "title": title,
    #         "headline": headline,
    #         "time": time,
    #         "author": author,
    #         "feature_img": feature_img,
    #         "description": description,
    #         "category": category,
    #         "URL": url,
    #     }
    
    # def sama_category(self, response):
    #     category = response.css(".breadcrumbs li::text").get()
    #     return category.split("|")[0]

    def parse_bol_news(self, response):
        title = response.css(".row h1::text").get()
        feature_img = response.css(".featuredimg img::attr(src)").get()
        description = response.css("div.changeMe p::text").getall()
        date = response.css(".date::text").get()


        yield {
            "title": title, 
            "feature_img": feature_img,
        }
    
    def parse_geo_news(self, response):
        title = response.css("div.story-area h1::text").get()
        headline = response.css("div.story-area h2::text").get()
        time = response.css("div.btSubTitle .post-time::text").get()
        author = response.css("div.btSubTitle .author_title_img a::text").get()
        feature_img = response.css("div.story-area .ui-sortable img::attr(src)").get()
        description = response.css("div.story-area .content-area p::text").getall()
        category = response.css("div.column-right a::attr(title)").get()
        url = response.url

        yield {
            "title": title,
            "headline": headline,
            "time": time,
            "author": author,
            "feature_img": feature_img,
            "description": description,
            "category": category,
            "URL": url,
        }
