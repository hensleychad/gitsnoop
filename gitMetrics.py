import pandas as pd
from sys import argv


def findDevelopers (dataFrame) :
    userDf = dataFrame.groupby(['committer_email'])['committer_name'].unique()
    userDff = dataFrame.groupby(['committer_name'])['committer_email'].unique()
    for  row in userDff.iteritems():
        print(row)

def determineActivity (dataFrame ):
    dataFrame['committer_date'] = pd.to_datetime(dataFrame['committer_date'])
    userDf = dataFrame.groupby(['committer_name'])['committer_date'].max()
    print (userDf)

def groupCommitsFileChangedByCommitter (dataFrame) :
    series = dataFrame.groupby(['committer_name','commit_hash'])['changed_file'].count()
    print(series)
    committerDf = series.to_frame().reset_index()
    committerDf = committerDf.rename(columns={'changed_file':'changed_file_count'})

    print(committerDf.head())
    return committerDf

def groupCommitsFileChangedByCommitterWithFilter (dataFrame ,filterBy) :
    filteredDf = (dataFrame[dataFrame['change_type'] == filterBy])
    print(filteredDf.head())
    series = filteredDf.groupby(['committer_name','commit_hash'])['changed_file'].count()
    print(series)
    committerDf = series.to_frame().reset_index()
    committerDf = committerDf.rename(columns={'changed_file':'changed_file_count'})

    print(committerDf.head())
    return committerDf

def countCommits (dataFrame) :
    totalCommitCount = 0
    totalFileChangedCount = 0

    countsDf = dataFrame.groupby(['committer_name'])\
    .agg({'commit_hash': 'count', 'changed_file_count': 'sum'})\
    .reset_index()

    print("committer_name,commit_hash,changed_file_count")
    for index, row in countsDf.iterrows():
        print("{},{},{}".format(row['committer_name'],row['commit_hash'],row['changed_file_count']))
        totalCommitCount+=row['commit_hash']
        totalFileChangedCount+=row['changed_file_count']

    return totalCommitCount, totalFileChangedCount, countsDf

def getFileChangedMedian (committerDf):

    medianDf = committerDf.groupby('committer_name')[['changed_file_count']].median()
    print(medianDf)

def getFileChangedAverage (countsDf) :
    fileChangedAverage = 0.0

    print("Committer Name, File Changed Average")
    for index, row in countsDf.iterrows():
        fileChangedAverage = row['changed_file_count'] / row ['commit_hash']
        print("{}, {}".format(row['committer_name'],fileChangedAverage))

def getRatios (totalCommitCount, totalFileChangedCount, countsDf):
    commitRatio = 0.0;
    changedFileRatio = 0.0;

    print("Committer Name, Commit Ratio ,File Changed Ratio")
    for index, row in countsDf.iterrows():
        commitRatio = row['commit_hash'] / totalCommitCount * 100
        changedFileRatio = row['changed_file_count'] / totalFileChangedCount * 100
        print("{},{}, {}".format(row['committer_name'],commitRatio,changedFileRatio))
        commitRatio = 0.0;
        changedFileRatio = 0.0;

if __name__ == "__main__":
  transactionFile = argv[1]
  commitsWithZeroChangeCount = int(argv[2])  # pass this in, there are commits without changes but tracking them anyway
  changedFilesFromRevListCount = int(argv[3])  # pass this in

  dataFrame = pd.read_csv(transactionFile)

  determineActivity(dataFrame)

  findDevelopers(dataFrame)
  committerDf = groupCommitsFileChangedByCommitter(dataFrame)
  getFileChangedMedian(committerDf);
  totalCommitCount, totalFileChangedCount, countsDf  = countCommits(committerDf)
  getRatios (commitsWithZeroChangeCount, changedFilesFromRevListCount, countsDf)
  getFileChangedAverage (countsDf)

  print("Finding Average & Medians for Adds\n")
  addDataFrame = groupCommitsFileChangedByCommitterWithFilter(dataFrame, "ModificationType.ADD")
  getFileChangedMedian(addDataFrame);
  totalCommitCount, totalFileChangedCount, addCountsDf  = countCommits(addDataFrame)
  getFileChangedAverage (addCountsDf)

  print("Finding Average & Medians for Modifies\n")
  modifyDataFrame = groupCommitsFileChangedByCommitterWithFilter(dataFrame, "ModificationType.MODIFY")
  getFileChangedMedian(modifyDataFrame);
  totalCommitCount, totalFileChangedCount, modifyCountsDf  = countCommits(modifyDataFrame)
  getFileChangedAverage (modifyCountsDf)

  print("Finding Average & Medians for Deletes\n")
  deleteDataFrame = groupCommitsFileChangedByCommitterWithFilter(dataFrame, "ModificationType.DELETE")
  getFileChangedMedian(deleteDataFrame)
  totalCommitCount, totalFileChangedCount, deleteCountsDf  = countCommits(deleteDataFrame)
  getFileChangedAverage (deleteCountsDf)
