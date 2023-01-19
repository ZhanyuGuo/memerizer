import pandas as pd
from pandas import DataFrame

excel_file = "./gre.xlsx"
data = pd.read_excel(excel_file)
print(data.loc[1, 'forget'])
data.loc[1, 'forget'] = 1
print(data.loc[1, 'forget'])

# data = data.fillna(0)
data.to_excel(excel_file, index=False)
