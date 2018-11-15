import pandas as pd
from sys import argv


def groupJiraGit (dataFrame):
   jiraGit = {}
   jiraGitSeries = dataFrame.groupby(['jiraTicket', 'commit_hash','change_type'])['new_path'].count()
   jiraGitSeries.to_dict()

   for item in jiraGitSeries.iteritems():
     jiraTicket = item[0][0]
     if jiraTicket not in jiraGit:
       jiraGit[jiraTicket] = {'commit': item[0][1], 'add':0, 'modify':0, 'delete':0}
       if item[0][2] =='ModificationType.ADD':
         jiraGit[jiraTicket]['add'] =  jiraGit[jiraTicket]['add'] + item[1]
       if item[0][2] =='ModificationType.MODIFY':
         jiraGit[jiraTicket]['modify'] =  jiraGit[jiraTicket]['modify'] + item[1]
       if item[0][2] =='ModificationType.DELETE':
         jiraGit[jiraTicket]['delete'] =  jiraGit[jiraTicket]['delete'] + item[1]
     else :
       if item[0][2] =='ModificationType.ADD':
           jiraGit[jiraTicket]['add'] =  jiraGit[jiraTicket]['add'] + item[1]
       if item[0][2] =='ModificationType.MODIFY':
           jiraGit[jiraTicket]['modify'] =  jiraGit[jiraTicket]['modify'] + item[1]
       if item[0][2] =='ModificationType.DELETE':
           jiraGit[jiraTicket]['delete'] =  jiraGit[jiraTicket]['delete'] + item[1]
       jiraGit[jiraTicket]['commit'] =  jiraGit[jiraTicket]['commit'] + "," + item[0][1]
   return (jiraGit)

if __name__ == "__main__":
    transactionFile = argv[1]
    dataFrame = pd.read_csv(transactionFile)
    jiraGit =  groupJiraGit (dataFrame)
    for row in jiraGit.items():
      print ("{}|{}|{}|{}|{}".format(row[0], row[1]['commit'],row[1]['add'],row[1]['modify'],row[1]['delete']))
