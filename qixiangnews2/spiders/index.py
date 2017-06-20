import scrapy
from qixiangnews2.items import Qixiangnews2Item
from scrapy.http import Request
from scrapy.spiders import CrawlSpider,Rule

class QiuBaiSpider(scrapy.Spider):
    name = 'qixiangnews'
    start_urls =[
        "http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/",
        'http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/index_1.html',
        'http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/index_2.html'
    ]

    def parse(self, response):
        for ele in response.xpath('//td[@class="nblue"]/a'):
            # titles = ele.xpath('./a/text()').extract()
            # a_node = ele.xpath('./a')
            titles = ele.xpath("string(.)").extract()
            hrefs =ele.xpath('./@href').extract()[0]
            print(hrefs)
            detail_url = response.urljoin(hrefs)
            req = Request(detail_url, callback=self.parse_detail)
            item = Qixiangnews2Item()
            item['href'] = hrefs
            item['title'] = titles
            req.meta['item'] = item
            yield req

    def parse_detail(self, response):
        item = response.meta["item"]
        item['date'] = response.xpath('//div[@class="news_textspan"]/div/span[2]/text()').extract()
        yield item

            # yield Qixiangnews2Item(title=titles,href=hrefs)

        # for next_url in response.xpath('//div[@class="manu"]/a/@href'):
        #     next_full_url = response.urljoin(next_url)
        #     print(next_full_url)
        #     print(123)
        #     yield scrapy.Request(next_full_url, callback=self.parse)
