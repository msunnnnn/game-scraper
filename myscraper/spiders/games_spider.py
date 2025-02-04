import scrapy


class GamesSpider(scrapy.Spider):
    name = "games"
    start_urls = [
        "https://www.playworks.org/game-library/?page=1&per_page=9&orderby=name&order=ASC&post_type=game",
    ]



    def parse(self, response):
        game_page_links = response.css("figure.card__figure a::attr(href)")
        yield from response.follow_all(game_page_links, self.parse_games)

        pagination_links = response.css("a.pagination__next")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_games(self, response):
        def extract_with_css(query):
            return response.css(query).get()
        
        def extract_with_css_dict(query):
            return response.css(query).getall()


        yield {
            "title": extract_with_css("h1::text"),
            "grade": extract_with_css("li.game__term--game-age strong::text"),
            "group_size": extract_with_css("li.game__term--game-group-size strong::text"),
            "equipment": extract_with_css("li.game__term--game-equipment strong::text"),
            "time": extract_with_css("li.game__term--game-length strong::text"),
            "setup": extract_with_css_dict("div.game__before-you-start ul li::text"),
            "instructions": extract_with_css_dict("div.game__how-to-play ul li::text"),
            "tags": extract_with_css_dict("a.pills__link::text"),
            
        }