#!/usr/bin/python3

import regex as re
from requests import Session
from sys import exit
from os import listdir
from typing import List
from datetime import date

class gear:
    """ Represents each product.
    Each attribute is scraped from
    the product webpage """

    __attrs__ = [
        "product_code",
        "title",
        "brand",
        "available",
        "price_actual",
        "price_regular",
        "material",
    ]

    def __init__(self,product_code=None,title=None,
            brand=None,available=None,price_actual=None,
            price_regular=None,material=None,url=None):

        self.product_code = product_code
        self.title = title
        self.brand = brand
        self.available = available
        self.price_actual = price_actual
        self.price_regular = price_regular
        self.material = material

    def __str__(self):
        return  f'Product code: {self.product_code}\n' + \
                f'Title: {self.title}\n' + \
                f'Brand: {self.brand}\n' + \
                f'Available: {self.available}\n' + \
                f'Discounted Price: {self.price_actual}\n' + \
                f'Regular Price: {self.price_regular}\n' + \
                f'Material: {self.material}\n'

    def strCSV(self):
        """ Prints gear data in CSV form """
        return  f'{self.product_code}	' + \
                f'{self.title}	' + \
                f'{self.brand}	' + \
                f'{self.available}	' + \
                f'{self.price_actual}	' + \
                f'{self.price_regular}	' + \
                f'{self.material}\n'

class muaythaifactory:
    """ Scraper for muaythaifactory.com.
    
    Example usage:
    muaythaifactory('mma-gloves').getAllGear()
    to scrape for all MMA gloves.
    """
    __attrs__ = [ "domain",
        "session",
        "working_url",
    ]

    GEAR_DICT = {
        'all-shorts': 'muay-thai-shorts.asp',
        'muay-thai-shorts': 'muay-thai-shorts.asp?typeid=1',
        'boxing-shorts': 'boxing-trunks.asp?typeid=2',
        'mma-shorts': 'mma-board-shorts.asp?typeid=12',
        'all-gloves': 'muay-thai-gloves.asp',
        'muay-thai-gloves': 'muay-thai-gloves.asp?typeid=20',
        'bag-gloves': 'muay-thai-gear.asp?typeid=28',
        'mma-gloves': 'grappling-mma-gloves.asp?typeid=29',
        'shins': 'muay-thai-equipment.asp?typeid=23',
        'wraps': 'muay-thai-gear.asp?typeid=25',
        'kick-pads': 'muay-thai-gear.asp?typeid=21',
        'focus-pads': 'muay-thai-gear.asp?typeid=22'
    }

    DOMAIN = 'https://www.muaythaifactory.com/'
    ERR_PAGE = 'https://www.muaythaifactory.com/?E=SNOTFOUND'
    CSV_PATH = './csv/'

    def __init__(self,gear_type=''):
        self.working_url = ''
        self.session = Session()
        self.setGearType(gear_type)

    def __enter__(self):
       return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def setGearType(self,gear_type):
        """ Sets the working url and gear_type attributes.
        Note that the input checks the GEAR_DICT constant to see whether
        the input gear_type is valid """

        try:
            self.working_url = self.DOMAIN + self.GEAR_DICT[gear_type]
            self.gear_type = gear_type

        except KeyError:
            print("Gear Type not found. Valid gear types are as follow:")
            for key, value in self.GEAR_DICT.items():
                print("- " + key)

            exit(1)

    def getPage(self,url) -> str:
        """ Returns page html of input url """

        try:
            if (self.working_url == ''):
                raise RuntimeWarning

            response = self.session.get(url)

            if (response.status_code == 200):
                if (response.url == self.ERR_PAGE):
                    return None
                else:
                    return response.text
            else:
                raise IndexError

        except IndexError:
            print("Couldn't get to webpage:" + url)
            exit(1)

        except RuntimeWarning:
            print("Please set geartype by using method: 'setGearType(<gear_type>)'")
            exit(1)

    def findAllProductCodes(self) -> List[str]:
        """ For the input gear_type, scrapes all pages for products codes
        and returns a list of all product codes """

        code_list = []

        curr_url = self.working_url
        curr_page_html = self.getPage(curr_url)

        max_page = self.getGearListPages(curr_page_html)
        code_list.extend(self.scrapeProductCodes(curr_page_html))

        for curr_page in range(1,max_page+1):
            curr_url = self.insertPageNumber(self.working_url,curr_page)

            curr_page_html = self.getPage(curr_url)

            code_list.extend(self.scrapeProductCodes(curr_page_html))

        return set(code_list)

    def getGearListPages(self,page0) -> int:
        pattern = re.compile(r'(?<=page \d+ of )\d+')
        return int(pattern.search(page0).group())

    def scrapeProductCodes(self,html:str) -> List[str]:
        pattern = re.compile(r'(?<=class="browse-product-code">).+(?=<\/span>)')
        return set(pattern.findall(html))

    def insertPageNumber(self,url,page_no) -> str:
        if (page_no == 1):
            return url
        elif not ('?' in url):
            return url + '?page=' + str(page_no)
        else:
            return url + '&page=' + str(page_no)

    def scrapeTypeIDs(self,limit=10):
        typeid_anchor = 'muay-thai-gear.asp?typeid='

        for i in range(1,limit):
            curr_url = self.DOMAIN + typeid_anchor + str(i)

            title = self.scrapeGearType(self.getPage(curr_url)).strip()

            if not (title == 'Muay Thai Products Search'):
                print("typeid: " + str(i) + ", title: " + title)

    def scrapeGearType(self,html) -> str:
        pattern = re.compile(r'(?<=<h2 class="c2-c1 no-margin-bottom"> *)\w.+')

        return pattern.search(html).group()

    def findProductURLs(self,page) -> List[str]:
        pattern = re.compile(r'(?<=<a href=").+(?=" class="prod_link")')
        return set(pattern.findall(page))

    def findAllProductURLs(self) -> List[str]:
        prod_urls = []

        curr_url = self.working_url
        anchor_ini = '&page='

        if not ('?' in self.working_url):
            anchor_ini = '?page='

        anchor_ini = '?page='
        curr_page_html = self.getPage(curr_url)

        max_page = self.getGearListPages(curr_page_html)

        prod_urls.extend(self.findProductURLs(curr_page_html))

        for i in range(2,max_page+1):
            anchor = anchor_ini + str(i)

            curr_url = self.working_url + anchor

            curr_page_html = self.getPage(curr_url)

            prod_urls.extend(self.findProductURLs(curr_page_html))

        return set(prod_urls)

    def getAllGear(self) -> List[gear]:
        gear_list = []
        prod_codes = self.findAllProductCodes()

        for code in prod_codes:
            if (curr_gear := self.getGearInfo(code)) is not None:
                gear_list.append(curr_gear)

        return gear_list

    def csvAllGear(self):
        csv_name = self.gear_type + str(date.today()) + '.csv'

        with open(self.CSV_PATH + csv_name, 'w') as csvfile:
            prod_codes = self.findAllProductCodes()

            for code in prod_codes:
                if (curr_gear := self.getGearInfo(code)) is not None:
                    csvfile.write(curr_gear.strCSV())


    def getGearInfo(self,product_code) -> gear:
        url = self.DOMAIN + 'muay-thai-gear.asp?ProductID=' + product_code

        if (gear_page_html := self.getPage(url)) is None:
            return None

        title = self.scrapeTitle(gear_page_html)

        available = self.checkAvailable(gear_page_html)

        brand = self.scrapeBrand(gear_page_html)

        price_actual = self.scrapeActualPrice(gear_page_html)
        price_regular = self.scrapeRegularPrice(gear_page_html)

        material = self.scrapeMaterial(gear_page_html)

        return gear(product_code,title,brand,
                    available,price_actual,
                    price_regular,material)

    def scrapeTitle(self,html) -> str:
        pattern = re.compile(r'(?<=<h1 class="product-name" itemprop="name">).+(?=<\/h1>)')
        return pattern.search(html).group()

    def scrapeBrand(self,html) -> str:
        pattern = re.compile(r'(?<=<meta itemprop="name" content=")[\w\s]+(?=">)')
        return pattern.search(html).group()

    def scrapeActualPrice(self,html) -> float:
        pattern = re.compile(r'(?<=<span class="price-our-price"><span itemprop="price" content=")[.\d]+(?=">)')
        if (match := pattern.search(html)):
            return float(match.group())
        else:
            return None

    def scrapeRegularPrice(self,html) -> float:
        pattern = re.compile(r'(?<=<span class="price-regular-price">)[.\d]+(?= USD)')
        if (match := pattern.search(html)):
            return float(match.group())
        else:
            return None

    def scrapeMaterial(self,html) -> List[str]:
        pattern = re.compile(r'(?<=<span .+material.+>)[\w\s]{2,}(?=<\/span>)')
        return pattern.findall(html)

    def checkAvailable(self,html) -> bool:
        pattern = re.compile(r'This item is not available at the moment')
        if pattern.search(html):
            return False
        else:
            return True

    def checkForExistingCache(self):
        cache_list = listdir(self.CSV_PATH)
        pattern = re.compile(r'^' + re.escape(self.gear_type) + r'\d{4}-\d{2}-\d{2}\.csv$')

        for files in cache_list:
            if (pattern.match(files)):
                return True

        return False
