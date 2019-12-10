import pandas as pd

data = pd.read_csv(r'E:\AmazonPycharm\amazon\sortedDealIDs.csv')

data.drop_duplicates(inplace=True)
data.columns = ['id', 'other']
deal_list = []
# {"dealID":"ff7155cd"}
for each in data['id'].values:
    deal_list.append({"dealID":each})
print(deal_list)