import pandas as pd
import os

# data = pd.read_csv(r'E:\AmazonPycharm\amazon\sortedDealIDs.csv')
#
# data.drop_duplicates(inplace=True)
# data.columns = ['id', 'other']
# deal_list = []
# # {"dealID":"ff7155cd"}
# for each in data['id'].values:
#     deal_list.append({"dealID":each})
# print(deal_list)

data_path = r'E:\AmazonPycharm\others\data\30天平均前5000hk不含dining'

df = pd.DataFrame()
for each in os.listdir(data_path):
    file = data_path + "/" + each
    df = pd.concat([df, pd.read_excel(file)])
df.drop(columns=['Image'], inplace=True)
df.drop_duplicates(subset=['Sales Rank: 30 days avg.', 'Categories: Tree'], inplace=True)
df.to_excel(r'E:\AmazonPycharm\others\data\30天平均前5000hk不含dining\all_drop.xlsx')
print(df)

