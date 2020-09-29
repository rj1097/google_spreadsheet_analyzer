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


    def logReworkInfo(self):
        wkb_f = self.wkbname.replace('(',':').replace(')','')
        for key,value in self.__contentCreatorData.items():
            value.rwk1_added = max(0,value.rwk1 - self.lastReworkCount(key,1,"Assigned"))
            value.rwk1_submitted = max(0,value.rwk_sub_1 - self.lastReworkCount(key,1,"Submitted"))
            value.rwk2_added = max(0,value.rwk2 - self.lastReworkCount(key,2,"Assigned"))
            value.rwk2_submitted = max(0,value.rwk_sub_2 - self.lastReworkCount(key,2,"Submitted"))
            logging.info(f"{wkb_f}: $$Content_Creator: {key}, $$Rework 1 Assigned: {value.rwk1}")
            logging.info(f"{wkb_f}: $$Content_Creator: {key}, $$Rework 1 Submitted: {value.rwk_sub_1}")
            logging.info(f"{wkb_f}: $$Content_Creator: {key}, $$Rework 2 Assigned: {value.rwk2}")
            logging.info(f"{wkb_f}: $$Content_Creator: {key}, $$Rework 2 Submitted: {value.rwk_sub_2}")

    def writeToCsv(self):
        self.logReworkInfo()
        contentCreatorDict = {k:dict(v) for k,v in self.__contentCreatorData.items()}
        contentCreatorDf = pd.DataFrame(contentCreatorDict).transpose()
        # logging.info(contentCreatorDict)
        del contentCreatorDf['Entry']
        contentCreatorDf.to_csv(self.wkbname+"_content-creatorData.csv")

        reviewer1Dict = {k:dict(v) for k,v in self.__reviewerData['r1'].items()}
        reviewer2Dict = {k:dict(v) for k,v in self.__reviewerData['r2'].items()}
        # logging.info(reviewer1Dict)
        # logging.info(reviewer2Dict)
        reviewerDf = pd.DataFrame(reviewer2Dict).transpose()
        reviewerDf["Reviewer"] = "Reviewer 2"
        reviewer1Df = pd.DataFrame(reviewer1Dict).transpose()
        reviewer1Df["Reviewer"] = "Reviewer 1"

        reviewerDf = reviewerDf.append(reviewer1Df)
        del reviewerDf["Entry"]
        reviewerDf.to_csv(self.wkbname+"_reviewerData.csv")

    def lastReworkCount(self,name,rwk,verb):
        val = 0
        wkb_f = self.wkbname.replace('(',':').replace(')','')
        with open('_log.log', 'r', encoding="utf-8") as f:
            contents = f.read()
            pattern = re.compile(r"([0-9\/ :PM]{22}): INFO: [\w: ]+\s(%s: )\$*Content_Creator: %s[\w, ]+ \$*Rework %d %s: ([\d]+)"% (wkb_f,name,rwk,verb))
            matches = pattern.finditer(contents)
            for match in matches:
                pass
            try:
                val = int(match.group(3))
            except Exception as e:
                logging.warn(e)
            f.close()
        return val

    def __init__(self, wkbname):
        self.wkbname = wkbname
        logging.info(f'Processing {wkbname}')
        self.__wkb = Workbook.__gc.open(wkbname)

    def extractData(self):
        self.__reviewerData = {}
        self.__reviewerData['r1'] = {}
        self.__reviewerData['r2'] = {}
        self.__contentCreatorData = {}
        for i in tqdm(range(maxsheets)):
            try:
                data = self.__wkb.get_worksheet(i).get_all_values()
                wks = Worksheet(data, self.__contentCreatorData, self.__reviewerData)
                wks.updateCreatorDict()
                wks.updateReviewerDict()
            except Exception as e:
                logging.warn(str(e) + f" for sheet{i} in Workbook: {self.wkbname}")

        # logging.info(self.contentCreatorData)
        # logging.info(self.reviewerData['r1'])
        # logging.info(self.reviewerData['r2'])
    
