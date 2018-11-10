import pandas as pd
from sys import argv


def findDevelopers (dataFrame) :
    dataFrame = dataFrame['committer_name'].unique()

def groupCommitsFileChangedByCommitter (dataFrame) :
    series = dataFrame.groupby(['committer_name','commit_hash'])['changed_file'].count()
    committerDf = series.to_frame().reset_index()
    committerDf = committerDf.rename(columns={'changed_file':'changed_file_count'})
    return committerDf

def countCommits (dataFrame) :
    countsDf = dataFrame.groupby('committer_name')\
    .agg({'commit_hash': 'count', 'changed_file_count': 'sum'})\
    .reset_index()

    return countsDf

if __name__ == "__main__":
  transactionFile = argv[1]

  dataFrame = pd.read_csv(transactionFile)
  committerDf = groupCommitsFileChangedByCommitter(dataFrame)
  countCommits(committerDf)



