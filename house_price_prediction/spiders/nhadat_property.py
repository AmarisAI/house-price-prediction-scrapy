import scrapy
from googletrans import Translator
from scrapy.loader import ItemLoader
from house_price_prediction.items import NhadatPropertyItem
import re

from .nhadat import strip_emoji
import pandas as pd

import logging
logging.basicConfig(filename='./log/nhadat_propery.log',level=logging.DEBUG)

main_features_list = ['Place', 'Number of floors', 'Number of bedrooms', 'Toilet',
                      'Year Built', 'Deposit', 'Direction', 'Road in front of the house', 'Juridical',
                      'Project']
item_list = ['house_location', 'num_floors', 'num_bedrooms', 'num_toilets', 'year_of_construction',
             'deposit', 'direction', 'road_info', 'juridical', 'project']


class NhadatProperty(scrapy.Spider):
    name="nhadat_property_page"
    custom_settings = {
        'LOG_LEVEL' :'ERROR',
        'LOG_ENABLED' : True,
        'LOG_STDOUT' : True
    }
    translator=Translator()
    def start_requests(self):
        # url = 'https://www.nhadat.net/808127049/cho-thue-ban-can-ho-dich-vu-day-du-tien-nghi'
        # yield scrapy.Request(url=url, callback=self.parse)
        df=pd.read_csv('./data/home_page_output.csv',usecols=['house_link'])
        for index, line in enumerate(df['house_link']):
            urls=line.split(',')
            for i, url in enumerate(urls):
                yield scrapy.Request(url=url, callback=self.parse)


    def _get_title_information(self, response,item):
        item['house_name'] = self.translator.translate(strip_emoji(response.xpath('//h1[@class="title_h1"]/text()').extract()), src='auto', dest='en')
        item['house_name'] = [house_name.text for house_name in item['house_name']]

        item['house_usable_area'] = response.xpath('//div[@class="area_price pull-right text-right"]/p/span[@class="area_top"]/text()').extract()
        item['house_usable_area'] = [house_area.strip(' \r\n/') for house_area in item['house_usable_area']]

        item['house_price']=self.translator.translate(response.xpath('//div[@class="area_price pull-right text-right"]/p/span[@class="price_top"]/text()').extract(), src='auto', dest='en')
        item['house_price'] = [house_price.text.strip(' \r\n/') for house_price in item['house_price']]

        item['house_price_per_area']=self.translator.translate(response.xpath('//div[@class="area_price pull-right text-right"]/p[2]/text()').extract(),src='auto',dest='en')
        item['house_price_per_area'] = [house_price_per_area.text.strip('Price area: ~\r\n/') for house_price_per_area in item['house_price_per_area']]

        item['house_code'] = self.translator.translate(response.xpath('//div[@class="pull-left"]/p[@id="_post_code"]/text()').extract(), src='auto',dest='en')
        item['house_code'] = [house_code.text.strip('Code: \r\n/') for house_code in item['house_code']]
        #print(item)
        return item


    def _get_main_features(self,response,item):

        main_features=self.translator.translate(response.xpath('//div[@class="row Main_features"]/div/span[@class="name"]/text()').extract(),src="auto",dest='en')
        main_features = [main_feature.text for main_feature in main_features]
        # print(main_features)

        main_features_text=self.translator.translate(response.xpath('//div[@class="row Main_features"]/div/span[@class="text"]/text()').extract(),dest='en')
        main_features_text = [main_feature_text.text for main_feature_text in main_features_text]
        # print(main_features_text)
        for index, feature in enumerate(main_features_list):
            if feature in main_features:
                # print("feature",feature)
                item[item_list[index]]=main_features_text[main_features.index(feature)]
            else:
                # print("na feature",feature)
                item[item_list[index]] ='NA'
        return item


    def _get_utilities(self,response,item):

        utilities=response.xpath('//div[@class="row utility"]/div/ul/li').extract()
        utility_array=[]
        for utility in utilities:
            if "active" in utility:
                utility_array.append(1)
            else:
                utility_array.append(0)

        item['utilities']=utility_array
        return item


    def parse(self, response):
        print("scarping webpage",response.url)
        self.logger.info('scraping webpage %s', response.url)

        item=NhadatPropertyItem()
        translator = Translator()
        item['url']=response.url
        title_info=self._get_title_information(response,item)

        main_features=self._get_main_features(response,item)
        utilities=self._get_utilities(response,item)

        item['num_utilities']=len(item['utilities'])

        item['description']= self.translator.translate(strip_emoji(response.xpath('//div[@class="swptext"]/div/p/text()').extract()),dest='en')
        item['description']= [desc.text.strip(' /r/n') for desc in item['description']]
        self.logger.info('item %s', item)
        # print(item['description'])
        yield item


