import scrapy
from neuralcrawling.items import ProductItem

class CrawlingSpider(scrapy.Spider):
    name = "mycrawler"
    allowed_domains = ["laptopworld.vn"]
    start_urls = [ 
                'https://laptopworld.vn/laptop-games-do-hoa.html', 
                #'https://laptopworld.vn/laptop-van-phong.html'
                ]
    
    custom_settings = {
        'FEEDS': {
            'gaming_graphic_laptop.json': {'format': 'json', 'overwrite': True},
        }
    }

    def parse(self, response):
        products = response.css('div.p-container')
        for product in products:
            relative_url = product.css('a.p-name').attrib['href']

            if relative_url is not None:
                book_url = 'https://laptopworld.vn' + relative_url
                yield response.follow(book_url, callback = self.parse_product_page)

            '''yield {
                'product_name': product.css('a.p-name::text').get(),
                'price': product.css('span.p-old-price::text').get(),
                'url': product.css('a.p-name').attrib['href'],
            }'''

        next_page = response.css('div.paging a.current + a').attrib['href']

        if next_page is not None:
            next_page_url = 'https://laptopworld.vn' + next_page
            yield response.follow(next_page_url, callback = self.parse)

    def parse_product_page(self, response):
        product_items = ProductItem()

        product_items['manufacturer'] = response.css('div.content-top-detail-left h1::text').get()
        product_items['cpu_manufacturer'] = response.css('div.product-summary-content div.item ::text').get().split(':')[1].strip().replace('\xa0', ' ').split(' ')
        product_items['cpu_brand_modifier'] = response.css('div.product-summary-content div.item ::text').get().split(':')[1].strip().replace('\xa0', ' ').split(' ')
        product_items['cpu_generation'] = response.css('div.product-summary-content div.item ::text').get().split(':')[1].strip().replace('\xa0', ' ').split(' ')
        product_items['cpu_speed'] = response.css('div.product-summary-content div.item ::text').get().split(':')[1].strip().replace('\xa0', ' ').split(' ')
        product_items['ram'] = response.css('div.product-summary-content div.item + div.item ::text').get().split(':')[1].strip()
        product_items['ram_type'] = response.css('div.product-summary-content div.item + div.item ::text').get().split(':')[1].strip()
        product_items['bus'] = response.css('div.product-summary-content div.item + div.item ::text').get().split(':')[1].strip()
        product_items['storage'] = response.css('div.product-summary-content div.item + div.item + div.item ::text').get().split(':')[1].strip()
        product_items['screen_resolution'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip()
        product_items['screen_size'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip()
        #product_items['refresh_rate'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item ::text').get()
        product_items['gpu_manufacturer'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip()
        product_items['weight'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip()
        product_items['battery'] = response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip()
        product_items['price'] = response.css('div.price-chinhhang.d-flex.align-items div.content del::text').get()

        yield product_items
        '''{
            'title': response.css('div.content-top-detail-left h1::text').get(),
            'cpu': response.css('div.product-summary-content div.item ::text').get().split(':')[1].strip().replace('\xa0', ' ').split(' '),
            'ram': response.css('div.product-summary-content div.item + div.item ::text').get().split(':')[1].strip(),
            'storage': response.css('div.product-summary-content div.item + div.item + div.item ::text').get().split(':')[1].strip(),
            'display': response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip(),
            'battery': response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip(),
            'weight': response.css('div.product-summary-content div.item + div.item + div.item + div.item + div.item + div.item + div.item ::text').get().split(':')[1].strip(),
            'price': response.css('div.price-chinhhang.d-flex.align-items div.content del::text').get(),
        }'''