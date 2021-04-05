import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import GgermanamericanItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class GgermanamericanSpider(scrapy.Spider):
	name = 'germanamerican'
	start_urls = ['https://germanamerican.com/about/news-events/']

	def parse(self, response):
		post_links = response.xpath('//p[@class="text-right"]/a[@class="btn cta-btn"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="article-date"]/text()').get().strip()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//article[@class="mod-news-details"]//text()[not (ancestor::p[@class="article-date"] or ancestor::p[@class="news-back"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=GgermanamericanItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
