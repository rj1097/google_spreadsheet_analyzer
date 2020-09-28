from customlog import *
from workbook import *
from config import *
from time import sleep

def main():
    for w in workbooks:
        wkb = Workbook(w)
        wkb.extractData()

    wkb.writeToCsv()



if __name__ == "__main__": main()