import scrapy
import time
from qixiangnews2.items import Qixiangnews2Item
from scrapy.http import Request
from scrapy.spiders import CrawlSpider,Rule

class QiuBaiSpider(scrapy.Spider):
    name = 'qixiangimgnews'
    start_urls =[
        "http://www.cma.gov.cn/2011xzt/2017zt/20170502/index.html",
    ]

    def parse(self, response):
        print(123)
        ifamesrc = response.xpath('//div[@class="content1"]/table/tr[1]/td[3]/iframe/@src').extract()[0]
        ifamesrc2 = response.urljoin(ifamesrc)
        req = Request(ifamesrc2, callback=self.iframe_parse)
        yield req

    def iframe_parse(self,response):
        for ele in response.xpath('//div[@id="fader"]/ul/li/a'):
            # titles = ele.xpath('./a/text()').extract()
            # a_node = ele.xpath('./a')
            titles = ele.xpath('./img/@alt').extract()
            hrefs =ele.xpath('./@href').extract()[0]
            imgsrc = ele.xpath('./img/@src').extract()[0]
            print(hrefs)
            detail_url = response.urljoin(hrefs)
            req = Request(detail_url, callback=self.parse_detail)
            item = Qixiangnews2Item()
            item['href'] = detail_url
            item['title'] = titles
            imgsrc2 = response.urljoin(imgsrc)
            item['imgsrc'] = imgsrc2
            req.meta['item'] = item
            yield req

    def parse_detail(self, response):
        item = response.meta["item"]
        date_str = response.xpath('//div[@class="news_textspan"]/div/span[2]/text()').extract()[0] if response.xpath('//div[@class="news_textspan"]').extract() else "000000000000000000000"
        item['date'] = date_str[5:9]+date_str[10:12]+date_str[13:15]+date_str[16:18]+date_str[19:21]+"00"
        # print(item['date'])
        # item['date'] = response.xpath('//div[@class="news_textspan"]/div/span[2]/text()').extract()
        yield item

            # yield Qixiangnews2Item(title=titles,href=hrefs)

        # for next_url in response.xpath('//div[@class="manu"]/a/@href'):
        #     next_full_url = response.urljoin(next_url)
        #     print(next_full_url)
        #     print(123)
        #     yield scrapy.Request(next_full_url, callback=self.parse)
