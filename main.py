from scraper import *

def main():
    try:
        x = muaythaifactory('shorts')

        gear_list = x.getAllGear(2)
        print(len(gear_list))

        for items in gear_list:
            print(items)
        
        x.closeSession()
    except:
        print("ran into problem")
        x.closeSession()
        sys.exit(0)

if __name__ == "__main__":
    main()
