import scrapy
from googletrans import Translator
from house_price_prediction.items import NhadatSpiderItem
import re
RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)


def strip_emoji(text_list):
    stripped_text_list=[RE_EMOJI.sub(r'', text) for index, text in enumerate(text_list)]
    return stripped_text_list


class NhadatSpider(scrapy.Spider):
    name="nhadat_home_page"
    custom_settings = {
        'LOG_LEVEL' :'ERROR',
        'LOG_ENABLED' : True,
        'LOG_STDOUT' : True
    }


    def start_requests(self):
        for i in range(0,1275):
            yield scrapy.Request('https://www.nhadat.net/ban-can-ho/ho-chi-minh/?page=%d' % i)



    def parse(self, response):
        print("scraping webpage : ",response.url)
        item=NhadatSpiderItem()

        translator=Translator()

        initial_link='https://www.nhadat.net'

        item['url']=response.url

        item['house_link']=response.xpath('//div[@class="media-body media-middle"]/a/@href').extract()
        item['house_link'] = [initial_link+house_link for house_link in item['house_link']]


        item['house_name']=translator.translate(strip_emoji(response.xpath('//div[@class="media-body media-middle"]/a[@href]/h2[@class="title"]/text()').extract()),src='auto',dest='en')
        item['house_name']=[house_name.text for house_name in item['house_name']]

        item['house_location']=translator.translate(response.xpath('//div[@class="adrest"]/a[@href]/text()').extract(),dest='en')
        item['house_location'] = [house_location.text.strip() for house_location in item['house_location']]

        item['house_area']=response.xpath('//li[@class="dt"]/span[@class="cusw_number"]/text()').extract()

        item['num_bedroom']=translator.translate(response.xpath('//li[@class="pn"]/span[@class="cusw_number"]/text()').extract(),dest='en')
        item['num_bedroom'] = [num_bedroom.text for num_bedroom in item['num_bedroom']]

        item['date_posted']=response.xpath('//li[@class="day"]/span[@class="cusw_number"]/text()').extract()

        item['house_price']=translator.translate(response.xpath('//div[@class="price"]/text()').extract(),dest='en')
        item['house_price'] =[house_price.text for house_price in item['house_price']]

        item['house_price_area']=translator.translate(response.xpath('//div[@class="price-area"]/text()').extract(),dest='en')
        item['house_price_area']= [price_area.text+'2' for index,price_area in enumerate(item['house_price_area'])]
        #print(item)
        yield item

