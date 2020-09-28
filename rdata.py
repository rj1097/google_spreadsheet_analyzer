from customlog import *
from dataclasses import dataclass

@dataclass
class Rdata:
    entry: str
    status: int = 0
    def __str__(self):
        return f"""
        ########################################################################
        Entry: {self.entry}
        Status: {self.status}
        """

    def __iter__(self):
        yield 'Status', self.status
        yield 'Entry', self.entry
    
    @classmethod
    def checkApprove(cls,val):
        return (("approve" in val.lower() or "correct" in val.lower() or "recheck" in val.lower()) and "reject" not in val.lower()) or ("sent" in val.lower() and "not" not in val.lower())
