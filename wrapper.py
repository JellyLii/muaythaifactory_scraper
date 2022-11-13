#!/usr/bin/python3

import regex as re
import requests
import sys

class gear:
    def __init__(self,url,product_code,brand,price_acutal,price_regular):
        '''
        sizes
        size_chart
        '''

        self.url = url
        self.product_code = product_code
        self.brand = brand
        self.price_actual = price_acutal
        self.price_regular = price_regular


class muaythaifactory:
    def __init__(self,gear_type):
        self.domain = 'https://www.muaythaifactory.com/'

        try:
            if (gear_type == 'shorts'):
                self.path = 'muay-thai-shorts.asp'
            else:
                raise ValueError
        except:
            print("Wrong input, Failure awww")
            sys.exit(1)

        self.working_url = self.domain + self.path

    def getGearListPages(self,page0):
        pattern = re.compile(r'(?<=page \d+ of )\d+')
        return int(pattern.search(page0).group())

    def getPage(self,url):
        try:
            response = requests.get(url)

            if (response.status_code == 200):
                return response.text
            else:
                raise Error
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
        prod_code = self.getProdCode(url)

        gear_page_html = self.getPage(url)

        brand = self.getBrand(gear_page_html)
        price_actual = self.getActualPrice(gear_page_html)
        price_regular = self.getRegularPrice(gear_page_html)
        material = self.getMaterial(gear_page_html)

        return gear(url,prod_code,brand,price_actual,price_regular)

    def getProdCode(self,url):
        pattern = re.compile(r'(?<=ProductID=).+')
        return pattern.search(url).group()

    def getBrand(self,html):
        pattern = re.compile(r'(?<=<meta itemprop="name" content=")\w+(?=">)')
        return pattern.search(html).group()

    def getActualPrice(self,html):
        pattern = re.compile(r'(?<=<span class="price-our-price"><span itemprop="price" content=")[.\d]+(?=">)')
        return float(pattern.search(html).group())

    def getRegularPrice(self,html):
        pattern = re.compile(r'(?<=<span class="price-regular-price">)[.\d]+(?= USD)')
        return float(pattern.search(html).group())

    def getMaterial(self,html):
        pattern = re.compile(r'(?<=<div class="product-info-subtext "  >Material: <span id="material-single" data-code="1">)\w+(?=</span>)')
        return pattern.search(html).group()

