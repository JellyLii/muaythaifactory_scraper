from scraper import *

def main():
<<<<<<< HEAD
    gear_type = 'all-gloves'
=======
    gear_type = 'mma-gloves'
>>>>>>> a5d3dbe4602c9f5ed9973c5626312be8a79f5653

    with muaythaifactory(gear_type) as x:
        print(x.csv_filepath)

if __name__ == "__main__":
    main()

