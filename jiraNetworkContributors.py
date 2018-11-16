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

def printResults (userDict):
  final_row = ""
  count = 0
  for user_x in userDict:
    if (count == 40):
      break
    for user_y in sorted(userDict[user_x]) :
        final_row = final_row + "," + str(userDict[user_x][user_y])
    count = count + 1
    print (user_x, final_row)
    final_row = ""

def buildNetwork (userDict):
    # test keys exist
    user_xy = 'Andreas Lehmkuhler'
    user_yx = 'ASF'
    userDict[user_xy][user_yx] = userDict[user_xy][user_yx]  + 1
    userDict[user_yx][user_xy] = userDict[user_yx][user_xy]  + 1
    return userDict



if __name__ == "__main__":

  transactionFile = argv[1]
  df = pd.read_csv(transactionFile)
  ntwkDict = df.to_dict()

  uniqueUsersList = buildUniqueUserList(ntwkDict)
  userDict = initMatrix(uniqueUsersList)
  userNetworkDict = buildNetwork(userDict)

  printResults(userNetworkDict)





