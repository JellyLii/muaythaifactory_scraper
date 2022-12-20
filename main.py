from scraper import *

def main():
    gear_type = 'all-gloves'

    with muaythaifactory(gear_type) as x:
        print(x.csv_filepath)

if __name__ == "__main__":
    main()

