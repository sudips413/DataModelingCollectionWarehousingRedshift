import scrapy
from movies.items import MoviesItem

class MoviecollectionSpider(scrapy.Spider):
    name = "movieCollection"
    allowed_domains = ["imdb.com"]
    start_urls = "https://www.imdb.com"
    genres=['action','romance']

    def start_requests(self):
        urls=[]
        for genre in self.genres:
            urls.append(f"{self.start_urls}/search/title/?genres={genre}&languages=en&sort=user_rating,desc&title_type=feature")
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)


    def parse(self, response):
        try:
            movies_list=response.css('div.lister-list')
            for movie in movies_list:
                movies=movie.css('div.lister-item.mode-advanced')
                for items in movies:
                    rating=items.css("div.inline-block.ratings-imdb-rating strong::text").get()
                    runtime=items.css("span.runtime::text").get()
                    year=items.css('span.lister-item-year.text-muted.unbold::text').get()
                    title=items.css("h3.lister-item-header a::text").get()
                    genres=items.css("p.text-muted  span.genre::text").get()
                
                    for item in items.css('p.sort-num_votes-visible'):
                        reviews=item.css("span:nth-child(2)::text").get()
                        gross=item.css('span:nth-child(5)::text').get()
                        
                    yield{
                        'title':title,
                        'year':year,
                        'rating':rating,
                        'no_of_reviews':reviews,
                        'genres':genres,
                        'runtime':runtime,
                        'gross':gross,
                        
                    }
        except:
            print("Error")
            pass

        next_page = response.css('a.lister-page-next.next-page').attrib['href']
        next_page = f"{self.start_urls}/{next_page}"
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)  
