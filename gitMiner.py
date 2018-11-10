from pydriller import RepositoryMining, GitRepository
from datetime import datetime, timezone, timedelta
import yaml
from sys import argv

def getconfig ( configFile ):
    configHandler = openFile(configFile, "r")
    config=yaml.load(configHandler)
    return config

def openFile ( fileName, action ):
    return open(fileName, action)

def closeFile ( fileHandler ):
    fileHandler.close()


def mineBranch( repoPath , branch, startDate, stopDate, metaHandler):
    commitCount = 0
    fileChangeCount = 0
    marker = 1  # this is a marker used for reshaping

    for commit in RepositoryMining( repoPath, only_in_branch=branch,since=startDate, to=stopDate).traverse_commits():
          for modification in commit.modifications:
              metaHandler.write('{},{},{},{},{},{},{}\n'.format( commit.committer.name, commit.committer.email, commit.committer_date,
                                                                  modification.filename, modification.change_type,commit.hash,marker))
              fileChangeCount += 1
          commitCount += 1
    print ("Branch Name {},File Change {},Commit Count {}".format(branch, fileChangeCount, commitCount))
    return commitCount, fileChangeCount

if __name__ == "__main__":
    commitCount = 0
    finalCommitCount = 0
    fileChangeCount = 0
    finalFileChangeCount = 0

    configFile = argv[1]

    config = getconfig ( configFile )

    to_zone = timezone(timedelta(hours=config["TIME_ZONE_OFFSET"]))
    startDate = datetime(config["START_YEAR"], config["START_MONTH"], config["START_DAY"], 0, 0, 0, tzinfo=to_zone)
    stopDate = datetime(config["STOP_YEAR"], config["STOP_MONTH"], config["STOP_DAY"], 0, 0, 0, tzinfo=to_zone)


    metaHandler = openFile(config["META_FILE"], "w")
    countHandler = openFile(config["COUNT_FILE"], "w")

    metaHandler.write('committer_name,committer_email,committer_date,changed_file,change_type,commit_hash,marker\n')
    for branch in config["BRANCHES"]:
      commitCount, fileChangeCount =  mineBranch(config["LOCAL_REPO"], branch, startDate, stopDate, metaHandler)
      finalCommitCount += commitCount
      finalFileChangeCount += fileChangeCount
    closeFile(metaHandler)

    print ("Final Count ", finalCommitCount, finalFileChangeCount)
    countHandler.write ('finalCommitCount, finalFileChangeCount\n')
    countHandler.write ('{},{}'.format(finalCommitCount,finalFileChangeCount))
    closeFile(countHandler)
