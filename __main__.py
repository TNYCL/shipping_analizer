from mechanize import Browser
import json
from bs4 import BeautifulSoup as bs

class trendyol:
    link = 'https://www.trendyol.com'
    search_link = 'https://www.trendyol.com/sr?q={0}&qt={0}&st={0}&os=1'
    json_product_link = 'https://public.trendyol.com/discovery-web-productgw-service/api/productRecommendation/{}?size={}&version=2'
    json_search_link = 'https://public.trendyol.com/discovery-web-searchgw-service/v2/api/aggregations/sr?q={0}&qt={0}&st={0}&prc={min}-{max}&sst=PRICE_BY_ASC'
    review_link = 'https://public-sdc.trendyol.com/discovery-web-productgw-service/api/review/{}'
    seller_link = 'https://public-mdc.trendyol.com/discovery-sellerstore-webgw-service/v1/follow/?sellerId={}'

    b = Browser()
    b.set_handle_robots(False)
    b.addheaders = [('Referer', link), ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    keyword = str(input('Search keyword: '))
    min_range = str(input('Minimum price: '))
    max_range = str(input('Maximum price: '))

    b.open(json_search_link.format(keyword.replace(' ', '+'), min=min_range, max=max_range))
    data = bs(b.response().read(), "html.parser")

    def open_link(link):
        b.open(link)
        return bs(b.response().read(), "html.parser")

    class product:
        def __init__(self, object):
            obj = json.loads(object)
            self.output = obj['result']['aggregations']

    details = product(data.text)
    print('\nOutput')
    print('-'*20)
    for found in details.output:
        if found['group'] != 'CATEGORY': continue
        value = found['values']
        for values in value:
            id = values['id']
            title = values['text']
            count = values['count']
            url = values['url']
            print('\nCategory name: {} '.format(title))
            print('Stock: {} '.format(count))
            print('Link: {}'.format(link + url))
