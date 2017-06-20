import scrapy
from qixiangnews2.items import Qixiangnews2Item
from scrapy.http import Request


class QiuBaiSpider(scrapy.Spider):
    name = 'qixiangnews'
    start_urls =[
        "http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/",
        'http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/index_1.html',
        'http://www.cma.gov.cn/2011xzt/2017zt/20170502/2017050201/index_2.html'
    ]

    def parse(self, response):
        for ele in response.xpath('//td[@class="nblue"]'):
            # titles = ele.xpath('./a/text()').extract()
            a_node = ele.xpath('./a')
            titles = a_node.xpath("string(.)").extract()
            hrefs =ele.xpath('./a/@href').extract()
            detail_url = response.urljoin(hrefs)
            req = Request(detail_url,self.parse_detail)
            item = Qixiangnews2Item()
            req.meta['item'] = item
            yield req

            # yield Qixiangnews2Item(title=titles,href=hrefs)

        # for next_url in response.xpath('//div[@class="manu"]/a/@href'):
        #     next_full_url = response.urljoin(next_url)
        #     print(next_full_url)
        #     print(123)
        #     yield scrapy.Request(next_full_url, callback=self.parse)
