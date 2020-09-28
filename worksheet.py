from customlog import *
import pandas as pd
from cdata import *
from rdata import *

class Worksheet:

    def __intializeColumns(self):
        for i in range(0,len(self.__columnsList)):
            columnName = self.__columnsList[i].lower()
            if ("name" in columnName or "developer" in columnName) and ("creator" in columnName or "content" in columnName):
                self.__cNameCol = i
                # logging.info(f"Creator Name Column index:{i}")

            if "status" in columnName and ("creator" in columnName or "self" in columnName):
                self.__cStatusCol = i
                # logging.info(f"Creator Status Column index:{i}")

            if "1" in columnName and "reviewer":
                if "status"  in columnName:
                    self.__r1StatusCol = i
                    # logging.info(f"Reviewer1 Status Column index:{i}")
                elif "name" in columnName:
                    self.__r1Col = i
                    # logging.info(f"Reviewer1 Column index:{i}")
            if "2" in columnName and "reviewer":
                if "status"  in columnName:
                    self.__r2StatusCol = i
                    # logging.info(f"Reviewer2 Status Column index:{i}")
                elif "name" in columnName:
                    self.__r2Col = i
                    # logging.info(f"Reviewer2 Column index:{i}")

            if "status" in columnName and "educator" in columnName and "manager" in columnName and "date" not in columnName:
                self.__eStatusCol = i
                # logging.info(f"Educator Manager Status Column index:{i}")

            if "rework" in columnName:
                if "1" in columnName:
                    if "sub" in columnName:
                        self.__rwkSub1Col = i
                        # logging.info(f"Rework 1 Submission Column index:{i}")
                    else:
                        self.__rwk1Col = i
                        # logging.info(f"Rework 1 Column index:{i}")
                elif "2" in columnName:
                    if "sub" in columnName:
                        self.__rwkSub2Col = i
                        # logging.info(f"Rework 2 Submission Column index:{i}")
                    else:
                        self.__rwk2Col = i
                        # logging.info(f"Rework 1 Column index:{i}")
                    
    def __generateReviewerKey(self, r):
        temp = r.strip('/').lower()
        temp = temp.replace("correct","@correct")
        temp = temp.replace("approve","@approve")

        name = ''
        name = temp.split("@")[0]
        name = name.split("/")[0]
        name = name.strip(" ")

        if "submit" in name or "complete" in name or "approve" in name or "correct" in name or "sent" in name or "send" in name:
                    name = ''

        return name.lower()

    def updateCreatorDict(self):
        for index,row in self.__df.iterrows():
            name = row[self.__cNameCol].lower()
            if name != '' and (not name.isdigit()):
                if ("name" in name or "developer" in name) and ("creator" in name or "content" in name):
                    continue
                key = name.lower().strip(" ").strip("/")
                if key not in self.__creatorDict:
                    self.__creatorDict[key] = Cdata(name)
                
                status = row[self.__cStatusCol]
                if Cdata.checkSent(status):
                    self.__creatorDict[key].sent += 1
                
                if self.__r1Col != -1:
                    r1 = row[self.__r1Col] + "/" + row[self.__r1StatusCol]
                else:
                    r1 = row[self.__r1StatusCol]
                if Cdata.checkR1(r1):
                    self.__creatorDict[key].r1 += 1

                if self.__r2Col != -1:
                    r2 = row[self.__r2Col] + "/" + row[self.__r2StatusCol]
                else:
                    r2 = row[self.__r2StatusCol]
                if Cdata.checkR2(r2):
                    self.__creatorDict[key].r2 += 1

                ed_status = row[self.__eStatusCol]
                if Cdata.checkEdManager(ed_status):
                    self.__creatorDict[key].ed_manager += 1
                
                rwk1 = row[self.__rwk1Col]
                if Cdata.checkRwk1(rwk1):
                    self.__creatorDict[key].rwk1 += 1

                rwk1_sub = row[self.__rwkSub1Col]
                if Cdata.checkRwk1Sub(rwk1_sub):
                    self.__creatorDict[key].rwk_sub_1 += 1

                rwk2 = row[self.__rwk2Col]
                if Cdata.checkRwk2(rwk2):
                    self.__creatorDict[key].rwk2 += 1

                rwk2_sub = row[self.__rwkSub2Col]
                if Cdata.checkRwk2Sub(rwk2_sub):
                    self.__creatorDict[key].rwk_sub_2 += 1

    def __helperReviewerUpdate(self, df_r, rKey):
        if rKey == 'r1':
            statusCol = self.__r1StatusCol
        else:
            statusCol = self.__r2StatusCol

        for val in df_r:
            key = self.__generateReviewerKey(val)
            
            if self.__columnsList[statusCol].lower() not in val.lower():
                if key not in self.__reviewerDict[rKey]:
                    self.__reviewerDict[rKey][key] = Rdata(val)
                if Rdata.checkApprove(val):
                    self.__reviewerDict[rKey][key].status += 1

    def updateReviewerDict(self):
        if self.__r2Col != -1:
            df_r2 = self.__df[self.__r2Col] + '/' + self.__df[self.__r2StatusCol]
        else:
            df_r2 = self.__df[self.__r2StatusCol]

        if self.__r1Col != -1:
            df_r1 = self.__df[self.__r1Col] + '/' + self.__df[self.__r1StatusCol]
        else:
            df_r1 = self.__df[self.__r1StatusCol]
        
        self.__helperReviewerUpdate(df_r1, 'r1')
        self.__helperReviewerUpdate(df_r2, 'r2')

    def __init__(self, data, cDict, rDict):
        self.__df = pd.DataFrame(data)

        self.__creatorDict = cDict
        self.__reviewerDict = rDict

        self.__cNameCol = -1
        self.__cStatusCol = -1
        self.__r1StatusCol = -1
        self.__r1Col = -1
        self.__r2StatusCol = -1
        self.__r2Col = -1
        self.__eStatusCol = -1
        self.__rwk1Col = -1
        self.__rwkSub1Col = -1
        self.__rwk2Col = -1
        self.__rwkSub2Col = -1
        self.__columnsList = self.__df[self.__df[1] != ''].iloc[0,:]

        self.__intializeColumns()
        if self.__cNameCol == -1:
            raise ValueError("Invalid sheet")
