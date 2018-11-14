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
          print ("{},{},{},{}".format(i[0],i[1],j,resolvedDict[i]))
        else :
          print("{},{},{},{}".format(i[0],i[1],j,0))

    # gets 0 reported but # completed
    for i, j in resolvedDict.items():
        if i not in reportedDict:
            print("{},{},{},{}".format(i[0],i[1],0,j))

