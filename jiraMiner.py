from jira import JIRA



if __name__ == "__main__":

  options = { 'server': 'https://issues.apache.org/jira'}
  jira = JIRA(options)

  issues = jira.search_issues('project=MATH',maxResults=None)

  for issue in issues:
      print(issue);

