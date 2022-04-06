import scrapy
# from scrapy.crawler import CrawlerProcess
import datetime
import time
from datetime import datetime
import logging
from scrapy.utils.log import configure_logging 


start_time = datetime.now()


class SomeSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )


class BookSpider(scrapy.Spider):
  name = 'book24'
  start_urls = ['https://book24.ru/catalog/']

  
  def parse(self, response):
    
      for link in response.css('div.product-card__image-holder a::attr(href)'):
        yield response.follow(link, callback=self.parse_book) 

      for i in range (1, 8661): 
        next_page = f'https://book24.ru/catalog/page-{i}/'
        yield response.follow(next_page, callback=self.parse)

        
  def parse_book(self, response):
    if len(response.css('ul.product-characteristic__list ::text').getall()) > 0: # Значение == 0 даст книги у которых нет четкого описания на стр. товара
        lst = [' Автор: ',' Серия: ', ' Раздел: ',' Издательство: ', ' Издательский бренд: ',' ISBN: ',
        ' Количество страниц: ',' Переплет: ',' Формат: ',' Возрастное ограничение: ',' Переводчик: ',
        ' Вес: ',' Год издания: ',' Бумага: '] # словарь параметров
        count_buy_lst = []
        price_lst = []
        review_lst = []
        articul_lst = []
        type_lst = []
        name_lst = []

        # Обработаем запрос об описании товара на каждой странице в презентабельный вид
        dirty_lst = response.css('ul.product-characteristic__list ::text').getall() 
        while(', ' in dirty_lst) :
            dirty_lst.remove(', ') 
        lst = dirty_lst
        count_idx = 0 
        count = 0 
        metki = [' Автор: ',' Серия: ', ' Раздел: ',' Издательство: ', ' Издательский бренд: ',' ISBN: ',
            ' Количество страниц: ',' Переплет: ',' Формат: ',' Возрастное ограничение: ',' Переводчик: ',
            ' Вес: ',' Год издания: ',' Бумага: '] 
        lst_idx = [] 
        lst_final = []

        while count_idx != len(metki):
            if metki[count_idx] in lst:
                lst_idx.append(lst.index(metki[count_idx])) 
            count_idx += 1
        lst_idx.append(len(lst)) 
        lst_idx = sorted(lst_idx) 

        while count != len(lst_idx)-1:
            lst_final.append(lst[lst_idx[count]:lst_idx[count+1]:]) 
            count += 1

        # Списки хелперы-посредники
        helper_authors_lst = []
        helper_series_lst = []
        helper_section_lst = []
        helper_publisher_lst = []
        helper_publisher_brand_lst = []
        helper_isbn_lst = []
        helper_count_pages_lst = []
        helper_cover_lst = []
        helper_format_lst = []
        helper_age_rating_lst = []
        helper_translators_lst = []
        helper_weight_lst = []
        helper_release_date_lst = []
        helper_paper_lst = []

        #  # Цикл по всему списку
        for i in range(len(lst_final)):
            if (' Автор: ' in lst_final[i]):
                authors = (lst_final[i][1:])
                helper_authors_lst.append(authors)
            else: 
                authors = 'NaN'
                helper_authors_lst.append(authors)

            if (' Серия: ' in lst_final[i]):
                series = (lst_final[i][1:])
                helper_series_lst.append(series)
            else: 
                series = 'NaN'
                helper_series_lst.append(series)
                
            if (' Раздел: ' in lst_final[i]):
                section = (lst_final[i][1:])
                helper_section_lst.append(section)
            else: 
                section = 'NaN'
                helper_section_lst.append(section)

            if (' Издательство: ' in lst_final[i]):
                publisher = (lst_final[i][1:])
                helper_publisher_lst.append(publisher)
            else: 
                publisher = 'NaN'
                helper_publisher_lst.append(publisher)

            if (' Издательский бренд: ' in lst_final[i]):
                publisher_brand = (lst_final[i][1:])
                helper_publisher_brand_lst.append(publisher_brand)
            else: 
                publisher_brand = 'NaN'
                helper_publisher_brand_lst.append(publisher_brand)

            if (' ISBN: ' in lst_final[i]):
                isbn = (lst_final[i][1:])
                helper_isbn_lst.append(isbn)
            else: 
                isbn = 'NaN'
                helper_isbn_lst.append(isbn)

            if (' Количество страниц: ' in lst_final[i]):
                count_pages = (lst_final[i][1:])
                helper_count_pages_lst.append(count_pages)
            else: 
                count_pages = 'NaN'
                helper_count_pages_lst.append(count_pages)

            if (' Переплет: ' in lst_final[i]):
                cover = (lst_final[i][1:])
                helper_cover_lst.append(cover)
            else: 
                cover = 'NaN'
                helper_cover_lst.append(cover)

            if (' Формат: ' in lst_final[i]):
                format = (lst_final[i][1:])
                helper_format_lst.append(format)
            else: 
                format = 'NaN'
                helper_format_lst.append(format)

            if (' Возрастное ограничение: ' in lst_final[i]):
                age_rating = (lst_final[i][1:])
                helper_age_rating_lst.append(age_rating)
            else: 
                age_rating = 'NaN'
                helper_age_rating_lst.append(age_rating)

            if (' Переводчик: ' in lst_final[i]):
                translators = (lst_final[i][1:])
                helper_translators_lst.append(translators)
            else: 
                translators = 'NaN'
                helper_translators_lst.append(translators)

            if (' Вес: ' in lst_final[i]):
                weight = (lst_final[i][1:])
                helper_weight_lst.append(weight)
            else: 
                weight = 'NaN'
                helper_weight_lst.append(weight)

            if (' Год издания: ' in lst_final[i]):
                release_date = (lst_final[i][1:])
                helper_release_date_lst.append(release_date)
            else: 
                release_date = 'NaN'
                helper_release_date_lst.append(release_date)

            if (' Бумага: ' in lst_final[i]):
                paper = (lst_final[i][1:])
                helper_paper_lst.append(paper)
            else: 
                paper = 'NaN'
                helper_paper_lst.append(paper)


        blank_authors_lst = [x for x in helper_authors_lst if x != 'NaN']        
        blank_series_lst = [x for x in helper_series_lst if x != 'NaN']
        blank_section_lst = [x for x in helper_section_lst if x != 'NaN']
        blank_publisher_lst = [x for x in helper_publisher_lst if x != 'NaN']
        blank_publisher_brand_lst = [x for x in helper_publisher_brand_lst if x != 'NaN']
        blank_isbn_lst = [x for x in helper_isbn_lst if x != 'NaN']
        blank_count_pages_lst = [x for x in helper_count_pages_lst if x != 'NaN']
        blank_cover_lst = [x for x in helper_cover_lst if x != 'NaN']
        blank_format_lst = [x for x in helper_format_lst if x != 'NaN']
        blank_age_rating_lst = [x for x in helper_age_rating_lst if x != 'NaN']
        blank_translators_lst = [x for x in helper_translators_lst if x != 'NaN']
        blank_weight_lst = [x for x in helper_weight_lst if x != 'NaN']
        blank_release_date_lst = [x for x in helper_release_date_lst if x != 'NaN']
        blank_paper_lst = [x for x in helper_paper_lst if x != 'NaN']


        if len(blank_authors_lst) == 0:
            blank_authors_lst.append('NaN')
        if len(blank_series_lst) == 0:
            blank_series_lst.append('NaN')
        if len(blank_section_lst) == 0:
            blank_section_lst.append('NaN')
        if len(blank_publisher_lst) == 0:
            blank_publisher_lst.append('NaN')
        if len(blank_publisher_brand_lst) == 0:
            blank_publisher_brand_lst.append('NaN')
        if len(blank_isbn_lst) == 0:
            blank_isbn_lst.append('NaN')
        if len(blank_count_pages_lst) == 0:
            blank_count_pages_lst.append('NaN')
        if len(blank_cover_lst) == 0:
            blank_cover_lst.append('NaN')
        if len(blank_format_lst) == 0:
            blank_format_lst.append('NaN')
        if len(blank_age_rating_lst) == 0:
            blank_age_rating_lst.append('NaN')
        if len(blank_translators_lst) == 0:
            blank_translators_lst.append('NaN')
        if len(blank_weight_lst) == 0:
            blank_weight_lst.append('NaN')
        if len(blank_release_date_lst) == 0:
            blank_release_date_lst.append('NaN')
        if len(blank_paper_lst) == 0:
            blank_paper_lst.append('NaN')

        #Количество купленных товаров
        if (len(response.css('p.product-detail-page__purchased-text::text').get()) > 0):
            if  ('раз' in response.css('p.product-detail-page__purchased-text::text').get().split()):
                count_buy_lst.append(response.css('p.product-detail-page__purchased-text::text').get().split()[1])
            elif('раза' in response.css('p.product-detail-page__purchased-text::text').get().split()):
                count_buy_lst.append(response.css('p.product-detail-page__purchased-text::text').get().split()[1])
            else:
                count_buy_lst.append('NaN')
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

        # Артикул товара
        if len(response.css('p.product-detail-page__article ::text')) == 1:
            articul_lst.append(response.css('p.product-detail-page__article ::text').getall()[0].split()[1])
        else:
            articul_lst.append('NaN')

        # Имя    
        if len(response.css('ol.breadcrumbs__list ::text').getall())> 2:
            type_lst.append(response.css("ol.breadcrumbs__list ::text")[1].get().strip())
            name_lst.append(response.css('ol.breadcrumbs__list ::text').getall()[-1].strip())
        elif len(response.css('ol.breadcrumbs__list ::text').getall()) == 2:
            type_lst.append('NaN')
            name_lst.append(response.css("ol.breadcrumbs__list ::text")[1].get().strip())
        else:
            type_lst.append('NaN')
            name_lst.append('NaN')

        yield{
        'author':blank_authors_lst[0],
        'name':name_lst[0],'type':type_lst[0],
        'articul':articul_lst[0],
        'buy':count_buy_lst[0],
        'price':price_lst[0],
        'review_star':review_lst,
        'series':blank_series_lst[0],
        'section':blank_section_lst[0],
        'publisher':blank_publisher_lst[0],
        'publisher_brand':blank_publisher_brand_lst[0],
        'ISBN':blank_isbn_lst[0],
        'count_pages':blank_count_pages_lst[0],
        'cover':blank_cover_lst[0],
        'format':blank_format_lst[0],
        'age_rating':blank_age_rating_lst[0],
        'translators':blank_translators_lst[0],
        'weight':blank_weight_lst[0],
        'release_year':blank_release_date_lst[0],
        'paper':blank_paper_lst[0]
        }

# current_datetime = datetime.now()
# name_book24 = 'book24_' + str(current_datetime.date()) + '__' + str(current_datetime.hour) + '-' + str(current_datetime.minute) + '.csv'

# c = CrawlerProcess(settings={
#   'FEED_URI' :name_book24,
#   'FEED_FORMAT': 'csv',
# })
# c.crawl(BookSpider)
# c.start() 

print('Время парсинга:', datetime.now() - start_time, ' с.')