#!/usr/bin/python3

import regex as re
import requests
import sys

class gear:

    __attrs__ = [
        "url",
        "product_code",
        "brand",
        "price_actual",
        "price_regular",
        "material",
    ]

    def __init__(self,url,product_code,brand,price_actual,price_regular,material):
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

class muaythaifactory:

    __attrs__ = [
        "domain",
        "err_page"
        "session",
        "gear_type",
        "path",
        "working_url",
    ]

    def __init__(self,gear_type=""):
        self.domain = 'https://www.muaythaifactory.com/'
        self.err_page = 'https://www.muaythaifactory.com/?E=SNOTFOUND'

        self.session = requests.Session()

        self.gear_type = gear_type
        self.path = ""
        self.working_url = ""

        if not(self.gear_type == ""):
            self.setGearType(self.gear_type)

    def closeSession(self):
        self.session.close()

    def setGearType(self,gear_type):
        #TODO: add all categories
        try:
            if (gear_type == 'shorts'):
                self.gear_type = 'shorts'
                self.path = 'muay-thai-shorts.asp'
            else:
                raise ValueError

            self.working_url = self.domain + self.path

        except:
            print("Wrong input, Failure aww")
            sys.exit(1)

    def getGearListPages(self,page0):
        pattern = re.compile(r'(?<=page \d+ of )\d+')
        return int(pattern.search(page0).group())

    def getPage(self,url):
        try:
            response = self.session.get(url)

            if (response.status_code == 200):
                if (response.url == self.err_page):
                    return None
                else:
                    return response.text
            else:
                raise IndexError
        except:
            print("Couldn't get to webpage:" + url)
            sys.exit(1)

    def findProductURLs(self,page):
        pattern = re.compile(r'(?<=<a href=").+(?=" class="prod_link")')
        return set(pattern.findall(page))

    def findAllProductURLs(self,limit=-1):
        prod_urls = []

        curr_url = self.working_url
        anchor_ini = '?page='

        curr_page_html = self.getPage(curr_url)
        print(curr_url)

        if (limit == -1):
            max_page = self.getGearListPages(curr_page_html)
        else:
            max_page = limit

        prod_urls.extend(self.findProductURLs(curr_page_html))

        for i in range(2,max_page+1):
            anchor = anchor_ini + str(i)

            curr_url = self.working_url + anchor
            print(curr_url)

            curr_page_html = self.getPage(curr_url)

            prod_urls.extend(self.findProductURLs(curr_page_html))

        return set(prod_urls)

    def getGearInfo(self,url):
        if (gear_page_html := self.getPage(url)) is None:
            return None
       
        prod_code = self.getProdCode(url)
        brand = self.getBrand(gear_page_html)
        price_actual = self.getActualPrice(gear_page_html)
        price_regular = self.getRegularPrice(gear_page_html)
        material = self.getMaterial(gear_page_html)

        return gear(url,prod_code,brand,price_actual,price_regular,material)

    def getAllGear(self,limit=-1):
        gear_list = []
        prod_urls = self.findAllProductURLs(limit)

        for url in prod_urls:
            if (curr_gear := self.getGearInfo(url)) is not None:
                gear_list.append(curr_gear)

        return gear_list

    def getProdCode(self,url):
        pattern = re.compile(r'(?<=ProductID=).+')
        return pattern.search(url).group()

    def getBrand(self,html):
        pattern = re.compile(r'(?<=<meta itemprop="name" content=")[\w\s]+(?=">)')
        return pattern.search(html).group()

    def getActualPrice(self,html):
        pattern = re.compile(r'(?<=<span class="price-our-price"><span itemprop="price" content=")[.\d]+(?=">)')
        return float(pattern.search(html).group())

    def getRegularPrice(self,html):
        pattern = re.compile(r'(?<=<span class="price-regular-price">)[.\d]+(?= USD)')
        return float(pattern.search(html).group())

    def getMaterial(self,html):
        pattern = re.compile(r'(?<=<span .+material.+>)[\w\s]{2,}(?=<\/span>)')
        return pattern.findall(html)
