from wrapper import *

def main():
    try:
        x = muaythaifactory('shorts')

        gear_list = x.getAllGear()
        print(len(gear_list))

        for items in gear_list:
            print(items.product_code)
        
        x.closeSession()
    except:
        print("ran into problem")
        x.closeSession
        sys.exit(0)

if __name__ == "__main__":
    main()
