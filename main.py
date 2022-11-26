from scraper import *

def main():
    gear_type = 'mma-gloves'
    with muaythaifactory(gear_type) as x:

        gear_list = x.csvAllGear()

if __name__ == "__main__":
    main()
