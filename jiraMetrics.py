import pandas as pd
from sys import argv

from datetime import datetime


def reporteddMonthlyReport (dataFrame):
    issueCreateSeries = dataFrame[dataFrame['issue_type'] == "Bug"].groupby(['issue_type','issue_created'])['issue_type'].count()
    return issueCreateSeries.to_dict()


def resolvedMonthlyReport (dataFrame):
    issueResolvedSeries = dataFrame[(dataFrame['issue_type'] == "Bug") & ((dataFrame['issue_status'] == "Resolved") | (dataFrame['issue_status'] == "Closed") )].groupby(['issue_type','resolved_date'])['issue_type'].count()
    return issueResolvedSeries.to_dict()

if __name__ == "__main__":
    transactionFile = argv[1]
    dataFrame = pd.read_csv(transactionFile)
    reportedDict = reporteddMonthlyReport (dataFrame)
    resolvedDict = resolvedMonthlyReport (dataFrame)

    for i, j in reportedDict.items():
        if i in resolvedDict:
          print ("{},{},{},{}\n".format(i[0],i[1],j,resolvedDict[i]))
        else :
            print("{},{},{},{}\n".format(i[0],i[1],j,0))
