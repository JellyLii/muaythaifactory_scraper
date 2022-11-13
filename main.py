from wrapper import *

def main():
    x = muaythaifactory('shorts')

    gear = x.getGearInfo('https://www.muaythaifactory.com/kids-muay-thai-shorts.asp?ProductID=ST-KS-100-BKGD')

    print(
    gear.url,
    gear.product_code,
    gear.brand,
    gear.price_actual,
    gear.price_regular,sep='\n')
    

if __name__ == "__main__":
    main()
