from jira import JIRA
import yaml
from sys import argv
import re

def openFile ( fileName, action ):
    return open(fileName, action)

def closeFile ( fileHandler ):
    fileHandler.close()

def getconfig ( configFile ):
    configHandler = openFile(configFile, "r")
    config=yaml.load(configHandler)
    return config

def formatDate (transDate):

    regex = r"(\d\d\d\d-\d\d)"
    match = re.search(regex, transDate)
    return match.group(0);



def formatJiraToCsv ( issues , metaHandler ):

    for issue in issues:
        issueResolved = "None"
        issueCreated = formatDate(issue.fields.created)
        issueUpdated = formatDate(issue.fields.updated)
        if issue.fields.resolutiondate:
          if issue.fields.resolution != "None":
           issueResolved = formatDate(issue.fields.resolutiondate)

        metaHandler.write('{},{},{},{},{},{}\n'.format(issue,issue.fields.issuetype.name,issue.fields.status,issueCreated,issueUpdated,issueResolved))

def formatJiraComments ( issue , metaHandler, users ):
    #for issue in issues:
        print("Issue -  ", issue)
        print(issue.raw['fields']['comment']['comments'])
        for comment in issue.fields.comment.comments:
            print("N Comment -  ", comment.author.name)
            print("D Comment -  ", comment.author.displayName)
            users += + "," + comment.author.displayName
            #print(issue.raw['fields']['comment']['comments'])
            #print( issue.fields.reporter.displayName)
        print("Users Network -  ", users)

def searchJiraProjectComments ( jiraServerUrl, projectId, untilDate ):
    options = {'server': jiraServerUrl}
    jira = JIRA(options)
    issues = jira.search_issues('project='+ projectId + ' AND created <= ' + untilDate ,maxResults=None,expand='changelog',fields = 'comment')
    return issues

def searchJiraProject( jiraServerUrl, projectId, untilDate ):
    options = {'server': jiraServerUrl}
    jira = JIRA(options)
    issues = jira.search_issues('project='+ projectId + ' AND created <= ' + untilDate ,maxResults=None)
    return issues

if __name__ == "__main__":
  configFile = argv[1]

  config = getconfig(configFile)
  metaHandler = openFile(config["META_FILE"], "w")

#  issueComments = searchJiraProjectComments(config['JIRA_URL'], config['JIRA_PROJECT_KEY'], config['UNTIL_DATE'])
  issues = searchJiraProject(config['JIRA_URL'], config['JIRA_PROJECT_KEY'], config['UNTIL_DATE'])

  metaHandler.write("issue_id,issue_type,issue_status,issue_created,issue_updated,resolved_date\n")
  formatJiraToCsv( issues , metaHandler)
#  formatJiraComments( issueComments , metaHandler)

  closeFile(metaHandler)
