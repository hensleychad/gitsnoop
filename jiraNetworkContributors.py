from sys import argv
import pandas as pd
import re


def removeDuplicates(duplicate):
  final_list = []
  for num in duplicate:
    if num not in final_list:
      final_list.append(num)
  return final_list

def buildUniqueUserList( ntwkDict ):
  usersList = []

  for i in ntwkDict['network']:
    userNetwork  = ntwkDict['network'][i]
    if (userNetwork):
      userNetworkList = userNetwork.split(',')
      uniqueUsersLists = removeDuplicates(userNetworkList)
      if (len(uniqueUsersLists) > 1):
        usersList = usersList + uniqueUsersLists
        #for uniqueUser in uniqueUserList:
  uniqueUsersList = removeDuplicates(usersList)
  return uniqueUsersList

def initMatrix( ntwkDict ):
  userDict = {}
  uniqueUsersLists = []
  for uniqueUser_x in uniqueUsersList:
    userDict[uniqueUser_x] = {uniqueUser_x: 0}
    for uniqueUser_y in uniqueUsersList:
      userDict[uniqueUser_x][uniqueUser_y] = 0
  return userDict

def printResults (userDict):
  final_row = ""

  print("User,",sorted(userDict))
  for user_x in sorted(userDict):
    for user_y in sorted(userDict[user_x]) :
        if (userDict[user_x][user_y] == 0):
          final_row = final_row + "," + "-"
        else:
           final_row = final_row + "," + str(userDict[user_x][user_y])
    print (user_x.rstrip(),final_row)
    final_row = ""

def buildNetwork (uniqueUsersList ,userDict):
    # test keys exist
    for uniqueUser_x in uniqueUsersList:
      for uniqueUser_y in uniqueUsersList:
        regex = r"(" + uniqueUser_y + ")"
        if re.search(regex, uniqueUser_x):
          count = 0 #this does nothing, do not feel like changing logic
        else:
          userDict[uniqueUser_x][uniqueUser_y] = userDict[uniqueUser_x][uniqueUser_y]  + 1
          userDict[uniqueUser_y][uniqueUser_x] = userDict[uniqueUser_y][uniqueUser_x]  + 1

    return userDict



if __name__ == "__main__":

  transactionFile = argv[1]
  df = pd.read_csv(transactionFile)
  ntwkDict = df.to_dict()
  userNetworkDict = {}

  uniqueUsersList = buildUniqueUserList(ntwkDict)
  userDict = initMatrix(uniqueUsersList)
  for i in ntwkDict['network']:
    userNetwork  = ntwkDict['network'][i]
    if (userNetwork):
      userNetworkList = userNetwork.split(',')
      uniqueUsersLists = removeDuplicates(userNetworkList)
      if (len(uniqueUsersLists) > 1):
        userNetworkDict = buildNetwork(uniqueUsersLists,userDict)
  printResults(userNetworkDict)

