import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ShoppingItem
import re
import datetime
import logging

current_year = datetime.datetime.today().year
current_day = datetime.datetime.today().day
current_month = datetime.datetime.today().month


class LidlSpider(scrapy.Spider):
    name = "lidl"
    allowed_domains = ["lidl.ie"]
    start_urls = ['https://www.lidl.ie/special-offers']
    link_extractor = LinkExtractor(allow=[r'https://www.lidl.ie/en/c/[^/]+/c\d+/w1'])

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield scrapy.Request(url=url, dont_filter=True)

    def parse(self, response):
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(
                url=link.url,
                callback=self.parse_event_bis
            )

    def parse_event_bis(self, response):

        products_in_page = response.css("div[data-id][data-name][data-price][data-currency][data-list]")
        item = ShoppingItem()
        for product in products_in_page:
            try:
                item['product_id'] = product.css("::attr(data-id)").extract()
                item['name'] = product.css("::attr(data-name)").extract()
                item['listing'] = product.css("::attr(data-list)").extract()
                item['price'] = product.css("::attr(data-price)").extract()
                item['currency'] = product.css("::attr(data-currency)").extract()
                item['tracking'] = product.css("::attr(data-tracking)").extract()
                item['tracking_type'] = product.css("::attr(data-tracking-type)").extract()
                item['description'] = product.css('.product__desc::text').get().strip()
                item['url'] = product.css('.product__body::attr(href)').get()
                item['crawl_date'] = datetime.datetime.today().isoformat()
                raw_week = product.css('.ribbon__text::text').get().strip()
                iso_week, week_number = self.get_week_date(raw_week=raw_week)
                item['iso_week'] = iso_week
                item['week_number'] = week_number

            except AttributeError as er:
                logging.exception(er)
                continue
            except Exception as er:
                logging.exception(er)
                continue
            yield item

    def get_week_date(self, raw_week: str) -> tuple:
        """
        raw date is in the formats
            "from 12.10"
            "12.01 - 18.10"
        returns isodate and week number
        """

        search_result = re.search(r'^(\d+.\d+)\s+-\s+\d+.\d+', raw_week)

        if "from" in raw_week:
            week = re.sub(r'^\D+', '', raw_week)

        elif search_result:
            week = search_result.group(1)
        else:
            week = "{}.{}".format(current_day, current_month)

        week_in_date_format_1900 = datetime.datetime.strptime(week, "%d.%m")
        currect_week = week_in_date_format_1900.replace(current_year)

        return currect_week.isoformat(), currect_week.isocalendar()[1]
