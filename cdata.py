from customlog import *
from dataclasses import dataclass

@dataclass
class Cdata:
    entry: str
    sent: int = 0
    r1: int = 0
    r2: int = 0
    ed_manager: int = 0
    rwk1: int = 0
    rwk_sub_1: int = 0
    rwk1_added = 0
    rwk1_submitted = 0
    rwk2: int = 0
    rwk_sub_2: int = 0
    rwk2_added = 0
    rwk2_submitted = 0

    def __str__(self):
        return f"""
            ###########################################################################
            Entry: {self.entry}
            Sent: {self.sent}
            Reviewer1: {self.r1}
            Reviewer2: {self.r2}
            Educator Manager: {self.ed_manager}
            Rework1:{self.rwk1}
            Rework Submission 1:{self.rwk_sub_1}
            Rework2:{self.rwk2}
            Rework Submission 2:{self.rwk_sub_2}
        """

    def __iter__(self):
        yield 'Entry', self.entry
        yield 'Sent', self.sent
        yield 'Reviewer 1', self.r1
        yield 'Reviewer 2', self.r2
        yield 'Educator Manager', self.ed_manager
        yield 'Rework 1', self.rwk1
        yield 'Rework Sub 1', self.rwk_sub_1
        yield 'New Rework 1 added', self.rwk1_added
        yield 'New Rework 1 submitted', self.rwk1_submitted
        yield 'Rework 2', self.rwk2
        yield 'Rework Sub 2', self.rwk_sub_2
        yield 'New Rework 2 added', self.rwk2_added
        yield 'New Rework 2 submitted', self.rwk2_submitted

    @classmethod
    def checkSent(cls,val):
        return "sen" in val.lower() and "not" not in val.lower()
    
    @classmethod
    def checkApprove(cls,val):
        return (("approve" in val.lower() or "correct" in val.lower() or "recheck" in val.lower()) and "reject" not in val.lower()) or ("sent" in val.lower() and "not" not in val.lower())
    
    @classmethod
    def checkR1(cls,val):
        return cls.checkApprove(val)

    @classmethod
    def checkR2(cls,val):
        return cls.checkApprove(val)

    @classmethod
    def checkEdManager(cls,val):
        return ("receive" in val.lower())
    
    @classmethod
    def checkRwk1(cls,val):
        val = val.strip('-')
        return val != ''
    
    @classmethod
    def checkRwk1Sub(cls,val):
        val = val.strip('-')
        return val != ''

    @classmethod
    def checkRwk2(cls,val):
        val = val.strip('-')
        return val != ''

    @classmethod
    def checkRwk2Sub(cls,val):
        val = val.strip('-')
        return val != ''