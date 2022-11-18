#!/usr/bin/python3

import regex as re
import requests
import sys
from typing import List

class gear:
    __attrs__ = [
        "url",
        "product_code",
        "brand",
        "price_actual",
        "price_regular",
        "material",
    ]

    def __init__(self,
            url,product_code,brand,
            price_actual,price_regular,
            material):
        '''
        sizes
        size_chart
        '''

        self.url = url
        self.product_code = product_code
        self.brand = brand
        self.price_actual = price_actual
        self.price_regular = price_regular
        self.material = material

    def __str__(self):
        return f'''URL: {self.url}\nProduct code: {self.product_code}
Brand: {self.brand}\nDiscounted Price: {self.price_actual}
Regular Price: {self.price_regular}\nMaterial: {self.material}\n'''

class muaythaifactory:

    __attrs__ = [
        "domain",
        "err_page",
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

    def __init__(self,gear_type=""):
        self.working_url = ''
        self.err_page = 'https://www.muaythaifactory.com/?E=SNOTFOUND'

        self.session = requests.Session()

        if not(gear_type == ""):
            self.setGearType(gear_type)

    def closeSession(self):
        self.session.close()

    def setGearType(self,gear_type):
        try:
            self.working_url = ''
            self.working_url = self.DOMAIN + self.GEAR_DICT[gear_type]

        except KeyError:
            self.working_url = ''

            print("Gear Type not found. Valid gear types are as follow:")
            for key, value in self.GEAR_DICT.items():
                print("- " + key)

            sys.exit(1)

    def getPage(self,url) -> str:
        try:
            if (self.working_url == ''):
                raise RuntimeWarning

            response = self.session.get(url)

            if (response.status_code == 200):
                if (response.url == self.err_page):
                    return None
                else:
                    return response.text
            else:
                raise IndexError
        except IndexError:
            print("Couldn't get to webpage:" + url)
            sys.exit(1)

        except RuntimeWarning:
            print("Please set geartype by using method: 'setGearType(<gear_type>)'")
            sys.exit(1)

    def scrapeTypeIDs(self,limit=10):
        typeid_anchor = 'muay-thai-gear.asp?typeid='

        for i in range(1,limit):
            curr_url = self.DOMAIN + typeid_anchor + str(i)

            title = self.getTitle(self.getPage(curr_url)).strip()

            if not (title == 'Muay Thai Products Search'):
                print("typeid: " + str(i) + ", title: " + title)

    def getGearListPages(self,page0) -> int:
        pattern = re.compile(r'(?<=page \d+ of )\d+')
        return int(pattern.search(page0).group())

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

    def getGearInfo(self,url) -> gear:
        if (gear_page_html := self.getPage(url)) is None:
            return None

        prod_code = self.getProdCode(url)
        print(prod_code)
        brand = self.getBrand(gear_page_html)
        print(brand)

        if self.checkAvailable(gear_page_html):
            price_actual = self.getActualPrice(gear_page_html)
            print(price_actual)
            print(price_regular)
        else:
            price_actual = None
            price_regular = None

        material = self.getMaterial(gear_page_html)
        print(material)

        output = gear(url,prod_code,brand,price_actual,price_regular,material)

        return output

    def getAllGear(self) -> List[gear]:
        gear_list = []
        prod_urls = self.findAllProductURLs()

        for url in prod_urls:
            if (curr_gear := self.getGearInfo(url)) is not None:
                gear_list.append(curr_gear)

        return gear_list

    def getProdCode(self,html) -> str:
        pattern = re.compile(r'(?<=ProductID=).+')
        return pattern.search(html).group()

    def getBrand(self,html) -> str:
        pattern = re.compile(r'(?<=<meta itemprop="name" content=")[\w\s]+(?=">)')
        return pattern.search(html).group()

    def getActualPrice(self,html) -> float:
        pattern = re.compile(r'(?<=<span class="price-our-price"><span itemprop="price" content=")[.\d]+(?=">)')
        return float(pattern.search(html).group())

    def getRegularPrice(self,html) -> float:
        pattern = re.compile(r'(?<=<span class="price-regular-price">)[.\d]+(?= USD)')
        return float(pattern.search(html).group())

    def getMaterial(self,html) -> List[str]:
        pattern = re.compile(r'(?<=<span .+material.+>)[\w\s]{2,}(?=<\/span>)')
        return pattern.findall(html)

    def getTitle(self,html) -> str:
        pattern = re.compile(r'(?<=<h2 class="c2-c1 no-margin-bottom"> *)\w.+')
        return pattern.search(html).group()

    def checkAvailable(self,html) -> bool:
        pattern = re.compile(r'This item is not available at the moment')
        if pattern.search(html):
            return True
        else:
            return False
