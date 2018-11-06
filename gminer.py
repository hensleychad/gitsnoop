from pydriller import RepositoryMining, GitRepository
from datetime import datetime, timezone, timedelta
import yaml

def getconfig ( configFile ):
    configHandler = openFile(configFile, "r")
    config=yaml.load(configHandler)
    return config

def openFile ( fileName, action ):
    return open(fileName, action)

def closeFile ( fileHandler ):
    fileHandler.close()


def mineRepo( repoPath , branch, startDate, stopDate, metaHandler):
    commitCount = 0
    fileChangeCount = 0

    metaHandler.write('Branch_name, developer, changed_file, change_type, commit_date, commit_hash \n')
    for commit in RepositoryMining(
        repoPath, only_in_branch=branch,since=startDate, to=stopDate).traverse_commits():
          for modification in commit.modifications:
              print('Branch {},Author {},modified {},change type {}, date {},commit {}'.format(branch, commit.author.name, modification.filename, modification.change_type, commit.committer_date,commit.hash))
              metaHandler.write('{},{},{},{},{},{} \n'.format(branch, commit.author.name, modification.filename, modification.change_type, commit.committer_date,commit.hash))
              fileChangeCount += 1
          commitCount += 1

    return commitCount, fileChangeCount

if __name__ == "__main__":
    commitCount = 0
    finalCommitCount = 0
    fileChangeCount = 0
    finalFileChangeCount = 0

    to_zone = timezone(timedelta(hours=5))
    startDate = datetime(2003, 5, 1, 0, 0, 0, tzinfo=to_zone)
    stopDate = datetime(2017, 11, 1, 0, 0, 0, tzinfo=to_zone)

    config = getconfig ( './config.yaml' )

    metaHandler = openFile(config["META_FILE"], "w")
    countHandler = openFile(config["COUNT_FILE"], "w")
    for branch in config["BRANCHES"]:
      commitCount, fileChangeCount = mineRepo(config["LOCAL_REPO"], branch, startDate, stopDate, metaHandler)
      finalCommitCount += commitCount
      finalFileChangeCount += fileChangeCount
    closeFile(metaHandler)

    print ("Final Count ", finalCommitCount, finalFileChangeCount)
    countHandler.write ('finalCommitCount, finalFileChangeCount\n')
    countHandler.write ('{},{}'.format(finalCommitCount ,finalFileChangeCount))
    closeFile(countHandler)
