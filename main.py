from scraper import *

def main():
    x = muaythaifactory('')
    x.setGearType('all-gloves')

    gear_list = x.getAllGear()

    for gear in gear_list:
        print(gear)
    
    x.closeSession()

if __name__ == "__main__":
    main()
