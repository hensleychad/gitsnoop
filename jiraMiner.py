from jira import JIRA
import yaml
from sys import argv

def openFile ( fileName, action ):
    return open(fileName, action)

def closeFile ( fileHandler ):
    fileHandler.close()

def getconfig ( configFile ):
    configHandler = openFile(configFile, "r")
    config=yaml.load(configHandler)
    return config

def formatJiraToCsv ( issues , metaHandler ):
    for issue in issues:
        print(issue.raw['fields'])
        metaHandler.write('{},{},{},{},{},{},{}\n'.format(issue,issue.fields.issuetype,issue.fields.status,
                                                  issue.fields.assignee,issue.fields.reporter.displayName,issue.fields.created,
                                                  issue.fields.updated,issue.fields.summary))

def formatJiraComments ( issues , metaHandler ):
    for issue in issues:
        print("Issue -  ", issue)
        for comment in issue.fields.comment.comments:
            print("N Comment -  ", comment.author.name)
            print("D Comment -  ", comment.author.displayName)
           # print("Comment -  ", issue.fields.name.displayName)
            #print(issue.raw['fields']['comment']['comments'])
            #print( issue.fields.reporter.displayName)

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

  issueComments = searchJiraProjectComments(config['JIRA_URL'], config['JIRA_PROJECT_KEY'], config['UNTIL_DATE'])
  issues = searchJiraProject(config['JIRA_URL'], config['JIRA_PROJECT_KEY'], config['UNTIL_DATE'])

  metaHandler.write("issue,issue_type,issue_status,issue_assignee,reporter,issue_created,issue_updated,issue_summary\n")

  formatJiraToCsv( issues , metaHandler)
  formatJiraComments( issueComments , metaHandler)

  closeFile(metaHandler)
