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
    marker = 1  # this is a marker used for reshaping

    print("Working on branch-", branch)
    for commit in RepositoryMining( repoPath, only_in_branch=branch,since=startDate, to=stopDate).traverse_commits():
          for modification in commit.modifications:
              metaHandler.write('{},{},{},{},{},{},{},{},{}\n'.format( commit.committer.name, commit.committer.email, commit.committer_date,
                                                                 modification.filename,modification.old_path,modification.new_path, modification.change_type,commit.hash,marker))

if __name__ == "__main__":

    configFile = argv[1]

    config = getconfig ( configFile )

    to_zone = timezone(timedelta(hours=config["TIME_ZONE_OFFSET"]))
    startDate = datetime(config["START_YEAR"], config["START_MONTH"], config["START_DAY"], 0, 0, 0, tzinfo=to_zone)
    stopDate = datetime(config["STOP_YEAR"], config["STOP_MONTH"], config["STOP_DAY"], 0, 0, 0, tzinfo=to_zone)

    metaHandler = openFile(config["META_FILE"], "w")
    metaHandler.write('committer_name,committer_email,committer_date,changed_file,old_path, new_path,change_type,commit_hash,marker\n')

    for branch in config["BRANCHES"]:
      mineBranch(config["LOCAL_REPO"], branch, startDate, stopDate, metaHandler)
    closeFile(metaHandler)
