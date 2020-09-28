import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from tqdm import tqdm
import re
from worksheet import Worksheet
from customlog import *
from config import maxsheets


class Workbook:
    __scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    __credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', __scope)

    __gc = gspread.authorize(__credentials)
    worksheets = __gc.openall()

    __reviewerData = {}
    __reviewerData['r1'] = {}
    __reviewerData['r2'] = {}
    __contentCreatorData = {}

    def __init__(self, wkbname):
        self.wkbname = wkbname
        logging.info(f'Processing {wkbname}')
        self.__wkb = Workbook.__gc.open(wkbname)

    def addSheet(self,*args):
        if not hasattr(self,'sheets'):
            self.sheets = []
        for idx in args:
            self.sheets.append(idx)
        logging.info(f'Sheets {self.sheets} added')

    def extractData(self):
        # self.reviewerData = {}
        # self.reviewerData['r1'] = {}
        # self.reviewerData['r2'] = {}
        # self.contentCreatorData = {}
        for i in tqdm(range(maxsheets)):
            try:
                data = self.__wkb.get_worksheet(i).get_all_values()
                wks = Worksheet(data, Workbook.__contentCreatorData, Workbook.__reviewerData)
                wks.updateCreatorDict()
                wks.updateReviewerDict()
            except Exception as e:
                logging.warn(str(e) + f" for sheet{i} in Workbook: {self.wkbname}")

        # logging.info(self.contentCreatorData)
        # logging.info(self.reviewerData['r1'])
        # logging.info(self.reviewerData['r2'])
    
    @classmethod
    def logReworkInfo(cls):
        for key,value in Workbook.__contentCreatorData.items():
            value.rwk1_added = value.rwk1 - cls.updateReworkStatus(key,1,"Assigned")
            value.rwk1_submitted = value.rwk_sub_1 - cls.updateReworkStatus(key,1,"Submitted")
            value.rwk2_added = value.rwk2 - cls.updateReworkStatus(key,2,"Assigned")
            value.rwk2_submitted = value.rwk_sub_2 - cls.updateReworkStatus(key,2,"Submitted")
            logging.info(f"$$Content_Creator: {key}, $$Rework 1 Assigned: {value.rwk1}")
            logging.info(f"$$Content_Creator: {key}, $$Rework 1 Submitted: {value.rwk_sub_1}")
            logging.info(f"$$Content_Creator: {key}, $$Rework 2 Assigned: {value.rwk2}")
            logging.info(f"$$Content_Creator: {key}, $$Rework 2 Submitted: {value.rwk_sub_2}")


    @classmethod
    def writeToCsv(cls):
        cls.logReworkInfo()
        contentCreatorDict = {k:dict(v) for k,v in Workbook.__contentCreatorData.items()}
        contentCreatorDf = pd.DataFrame(contentCreatorDict).transpose()
        logging.info(contentCreatorDict)
        del contentCreatorDf['Entry']
        contentCreatorDf.to_csv("content-creatorData.csv")

        reviewer1Dict = {k:dict(v) for k,v in Workbook.__reviewerData['r1'].items()}
        reviewer2Dict = {k:dict(v) for k,v in Workbook.__reviewerData['r2'].items()}
        logging.info(reviewer1Dict)
        logging.info(reviewer2Dict)
        reviewerDf = pd.DataFrame(reviewer2Dict).transpose()
        reviewerDf["Reviewer"] = "Reviewer 2"
        reviewer1Df = pd.DataFrame(reviewer1Dict).transpose()
        reviewer1Df["Reviewer"] = "Reviewer 1"

        reviewerDf = reviewerDf.append(reviewer1Df)
        del reviewerDf["Entry"]
        reviewerDf.to_csv("reviewerData.csv")

    @classmethod
    def updateReworkStatus(cls,name,rwk,verb):
        val = 0
        with open('_log.log', 'r', encoding="utf-8") as f:
            contents = f.read()
        #     print(contents)
            pattern = re.compile(r"([0-9\/ :PM]{22}): INFO: [\w: ]+\$*Content_Creator: %s[\w, ]+ \$*Rework %d %s: ([\d]+)"% (name,rwk,verb))
            matches = pattern.finditer(contents)
            for match in matches:
                pass
            try:
                val = int(match.group(2))
            except Exception as e:
                logging.warn(e)
            f.close()
        return val
