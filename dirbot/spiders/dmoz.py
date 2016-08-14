import scrapy

from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//div[@class="title-and-desc"]')
        items = []

        for site in sites:
            item = Website()
            item['title'] = site.xpath('a/text()').extract()
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('//div[@class="site-descr "]/text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items
