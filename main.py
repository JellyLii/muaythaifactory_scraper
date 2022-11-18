from scraper import *

def main():
    try:
        x = muaythaifactory('')
        x.setGearType('all-gloves')

        gear_list = x.getAllGear()

        for gear in gear_list:
            print(gear)
        
        x.closeSession()
    except:
        print("ran into problem")
        x.closeSession()
        sys.exit(0)

if __name__ == "__main__":
    main()
