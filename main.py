from customlog import *
from workbook import *
from config import *
from time import sleep

def main():
    for w in workbooks[0:1]:
        print("---------------------------------------------------------------------")
        print(w)
        wkb = Workbook(w)
        wkb.extractData()
        wkb.writeToCsv()
        # time.sleep(110)



if __name__ == "__main__": main()