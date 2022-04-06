import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# from scrapy.crawler import CrawlerProcess
import datetime
from datetime import datetime
import logging
from scrapy.utils.log import configure_logging 

class SomeSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

class BookSpider(CrawlSpider):
  name = 'book24_crawler'
  start_urls = ['https://book24.ru/']

  rules = (
      Rule(LinkExtractor(allow='catalog')),
      Rule(LinkExtractor(allow='product'), callback='parse_items')
  )
      
  def parse_items(self, response):
    lst = [' Автор: ',' Серия: ', ' Раздел: ',' Издательство: ', ' Издательский бренд: ',' ISBN: ',
    ' Количество страниц: ',' Переплет: ',' Формат: ',' Возрастное ограничение: ',' Переводчик: ',
    ' Вес: ',' Год издания: ',' Бумага: '] # словарь параметров
    second_lst = []
    count_buy_lst = []
    price_lst = []
    review_lst = []

    # Список переменных из 'lst'
    for i in range(len(lst)):
        if (lst[i] in response.css('ul.product-characteristic__list ::text').getall()):
            book_list = response.css('ul.product-characteristic__list ::text').getall()
            second_lst.append(book_list[book_list.index(lst[i]) + 1].strip())
        else:
            second_lst.append('NaN')    

    # Количество купленных товаров
    if  ('раз' in response.css('p.product-detail-page__purchased-text::text').get().split()):
        count_buy_lst.append(response.css('p.product-detail-page__purchased-text::text').get().split()[1])
    elif('раза' in response.css('p.product-detail-page__purchased-text::text').get().split()):
        count_buy_lst.append(response.css('p.product-detail-page__purchased-text::text').get().split()[1])
    else:
        count_buy_lst.append('NaN')

    # Цена товара
    if(len(response.css('div.product-sidebar-price__main-price ::text').getall())>0):
        price_describe_list = ' '.join(response.css('div.product-sidebar-price__main-price ::text').get().split())
        price_lst.append((price_describe_list[:-6])+(price_describe_list[-5:-2]))
    else:
        price_lst.append('NaN')

    # Оценка товара
    if (len(response.css('div.product-detail-page__more-information ::text').getall()[0].strip())>3):
        review_lst.append('NaN')
    else:
        review_lst.append(response.css('div.product-detail-page__more-information ::text').getall()[0].strip())
    
    type = response.css("ol.breadcrumbs__list ::text")[1].get().strip()
    name = response.css('ol.breadcrumbs__list ::text').getall()[-1].strip()
    yield{
    'author':second_lst[0],
    'name':name,'type':type,
    'buy':count_buy_lst[0],
    'price':price_lst[0],
    'review_star':review_lst,
    'series':second_lst[1],
    'section':second_lst[2],
    'publisher':second_lst[3],
    'publisher_brand':second_lst[4],
    'ISBN':second_lst[5],
    'count_pages':second_lst[6],
    'cover':second_lst[7],
    'format':second_lst[8],
    'age_rating':second_lst[9],
    'translator':second_lst[10],
    'weight':second_lst[11],
    'release_year':second_lst[12],
    'paper':second_lst[13]
    }

# current_datetime = datetime.now()
# name_book24 = 'book24_' + str(current_datetime.date()) + '__' + str(current_datetime.hour) + '-' + str(current_datetime.minute) + '.csv'

# c = CrawlerProcess(settings={
#   'FEED_URI' :name_book24,
#   'FEED_FORMAT': 'csv',
# })
# c.crawl(BookSpider)
# c.start() 

        
  