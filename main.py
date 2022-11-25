from scraper import *

def main():
    gear_type = 'all-gloves'
    with muaythaifactory(gear_type) as x:

        gear_list = x.getAllGear()

        for gear in gear_list:
            print(gear)

        
if __name__ == "__main__":
    main()
