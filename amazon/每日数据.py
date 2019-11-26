#!/usr/bin/env python
# coding: utf-8

# In[219]:


import pyecharts
import numpy as np 
import pandas as pd


file_list = []
for each in os.listdir():
    if each.startswith('业务报告') and each.endswith('csv'):
        file_list.append(each)


data_sum = pd.DataFrame()
for ffile in file_list:
    data_time = '2019-' + "-".join(ffile.split('-')[2:4])
    print(data_time)
    data = pd.read_csv(ffile)
    data['date'] = data_time
    data_sum = pd.concat([data_sum,data])


data_sum.columns = ['ASIN', 'sub_ASIN', '商品名称', '买家访问次数', '买家访问次数百分比', '页面浏览次数',
       '页面浏览次数百分比', '购买按钮赢得率', '已订购商品数量', '订购数量 – B2B', '订单商品数量转化率',
       '商品转化率 – B2B', '已订购商品销售额', '已订购商品的销售额 – B2B', '订单商品种类数',
       '订单商品总数 – B2B','date']

data_sum['date'].unique()


# In[225]:


# data_sum['date'] = pd.to_datetime(data_sum['date'])
data_sum


# In[226]:


data_info = data_sum[['date','ASIN','sub_ASIN','买家访问次数','商品转化率 – B2B','订购数量 – B2B','已订购商品的销售额 – B2B']]
data_info.head()


# In[227]:


def get_num(strr):
    strr = str(strr)
    return float(strr.strip('￥').replace(",",''))


# In[228]:


data_info['已订购商品的销售额 – B2B'] = data_info['已订购商品的销售额 – B2B'].apply(get_num)
data_info['买家访问次数'] = data_info['买家访问次数'].apply(lambda x: int(str(x).replace(',','')))
data_info['商品转化率 – B2B'] = data_info['商品转化率 – B2B'].apply(lambda x:float(str(x).strip('%'))*0.01)


# In[268]:


table_data = pd.pivot_table(data=data_info,columns=['ASIN','sub_ASIN'],
                            index=['date'],
                           values=['买家访问次数','商品转化率 – B2B','订购数量 – B2B','已订购商品的销售额 – B2B'])

data_info.to_excel('data_info.xlsx')

table_data.to_excel('table3.xlsx')


asin_list = list(data_info['ASIN'].unique())

from pyecharts import Page,Grid
data_page = Page()
for m in asin_list[1:3]:
    for n in data_info[data_info['ASIN'] == m]['sub_ASIN']:
#         print(data_info[data_info['ASIN'] == m])
        session_count_list = list(data_info[(data_info.ASIN == m) & (data_info.sub_ASIN ==  n)]['买家访问次数'])
        session_rate_list = list(data_info[(data_info.ASIN == m) & (data_info.sub_ASIN ==  n)]['商品转化率 – B2B'])
        goods_count_list = list(data_info[(data_info.ASIN == m) & (data_info.sub_ASIN ==  n)]['订购数量 – B2B'])
        goods_revenue_list = list(data_info[(data_info.ASIN == m) & (data_info.sub_ASIN ==  n)]['已订购商品的销售额 – B2B'])
        date_list = list(data_info[(data_info.ASIN == m) & (data_info.sub_ASIN ==  n)]['date'])
#         date_list = ['4-1','4-2','2019-4-18','2019-4-19']
        from pyecharts import Line
        line = Line(m)
        line.add(n,date_list,session_count_list)
        data_page.add(line)
data_page.render()

data['（子）ASIN'].value_counts()
