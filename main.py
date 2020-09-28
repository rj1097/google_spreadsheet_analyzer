from customlog import *
from workbook import *
from config import *
from time import sleep

def main():
    # logging.info("This is a info message")
    for w in workbooks[1:2]:
        wkb = Workbook(w)
        # wkb.addSheet(0)
        wkb.extractData()

    wkb.writeToCsv()



if __name__ == "__main__": main()