import pandas as pd
from sys import argv


def findDevelopers (dataFrame) :
    df = dataFrame['developer'].unique()
    print (df)


if __name__ == "__main__":
  transactionFile = argv[1]

  dataFrame = pd.read_csv(transactionFile)
  print (dataFrame.head())

  findDevelopers(dataFrame)

