from sys import argv
import pandas as pd


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
  #print (uniqueUsersList)
  for uniqueUser_x in uniqueUsersList:
    userDict[uniqueUser_x] = {uniqueUser_x: 0}
    count = 0
    for uniqueUser_y in uniqueUsersList:
      userDict[uniqueUser_x][uniqueUser_y] = 0
      if (count == 40):
        break
      count = count +1
  return userDict

if __name__ == "__main__":

  transactionFile = argv[1]
  df = pd.read_csv(transactionFile)
  ntwkDict = df.to_dict()

  uniqueUsersList = buildUniqueUserList(ntwkDict)
  userDict = initMatrix(uniqueUsersList)

  print (userDict)




