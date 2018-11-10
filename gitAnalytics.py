import pandas as pd
from sys import argv
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

def encode_units(x):
    if x >= 1.0:
        return 1
    else:
        return 0

def openFile ( fileName, action ):
    return open(fileName, action)

def closeFile ( fileHandler ):
    fileHandler.close()

def getItemSets ( dataFrame , minSupport ):
    dataFrameSet = dataFrame.applymap(encode_units)
    frequentItemsets = apriori(dataFrameSet, min_support=minSupport , use_colnames=True)

    return frequentItemsets

def fillBasket ( dataFrame ):
    dfBasket = (df[df['change_type'] == "ModificationType.MODIFY"]
                .drop(['committer_name', 'change_type'], axis=1)
                .groupby(['commit_hash', 'changed_file'])['marker']
                .sum().unstack().reset_index().fillna(0)
                .set_index('commit_hash'))
    print(dfBasket.head())
    return dfBasket

def showRules ( rules ):
    print('consequents,support,confidence,lift,conviction \n')
    for index,rule in rules.iterrows():
        print('{},{},{},{},{}'.format(rule['consequents'],rule['support'],rule['confidence'],rule['lift'],rule['conviction']))

if __name__ == "__main__":

  transactionFile = argv[1]
  minSupport = float(argv[2])

  df = pd.read_csv(transactionFile)

  dfBasket = fillBasket(df)
  itemSets = getItemSets(dfBasket, minSupport)
  rules = association_rules(itemSets, metric="lift", min_threshold=1)
  showRules(rules)
