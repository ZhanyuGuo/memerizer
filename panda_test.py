import pandas as pd
from pandas import DataFrame
from random import sample

excel_file = "./gre.xlsx"
data = pd.read_excel(excel_file)
print(data.loc[1, 'forget'])
data.loc[1, 'forget'] = 1
print(data.loc[1, 'forget'])
# wrongData = data[data['forget'] > 0]
# print(wrongData)
# print(len(wrongData))
wrongWord = data[data['forget'] > 100]
print(len(wrongWord))
# print(wrongWord.index[0])
# print(type(int(wrongWord.index[0])))

# ls = [1,2,5,4]
# words = data.iloc[ls]
# print(words)
# print(words.loc[5, 'word'])
# print(words.loc[5, 'word'].index)

# print(data['forget'] > 0)
# print(sample(list(data['forget'] > 0), 1))

# data = data.fillna(0)
# data.to_excel(excel_file, index=False)
