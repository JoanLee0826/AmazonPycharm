import numpy as np
import re
import pandas as pd
from pyecharts import charts as chas
from pyecharts import options as opts


file_path = r'E:\爬虫pycharm\data\goods_detail\10231420_with_ad.xlsx'
data_df = pd.DataFrame(pd.read_excel(file_path))
data_df.dropna(subset=['sales_est'], inplace=True)
data_df.sort_values(by=['sales_est'], inplace=True, ascending=False)
data_bar = (
    chas.Bar()
    .add_xaxis(data_df['ASIN'].tolist())
    .add_yaxis("预测销量", data_df['sales_est'].tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='销量预测'),
        legend_opts=opts.LegendOpts(is_show=True),
        toolbox_opts=opts.ToolboxOpts(),
        datazoom_opts=opts.DataZoomOpts(),   
    )
)

def money_change(strr):
    money_ = None
    if strr:
        try:
            money_ = float(strr.replace(',','').strip('$'))
        except:
            money_ = None
    if re.search(strr, '-'):
        try:
            strr_1, strr_2 = strr.split('-')
            money_ = np.mean((float(strr_1.replace(',', '').strip('$')), float(strr_2.replace(',','').strip('$'))))
        except:
            money_ = None

    return money_


# 转化价格为浮点数
price = data_df['goods_price'].map(money_change)
price_bins = [0, 15, 20, 25, 30, 35, 40, 100]
bins_values = pd.cut(price, bins=price_bins).value_counts()
e_bin_list = [(str(price_bins[m]) + '-' + str(price_bins[m+1]), n) for m,n in zip(range(len(price_bins)), bins_values.tolist())]

data_pie = (
    chas.Pie()
    .add("价格区间", 
         e_bin_list,
         center=['50%', '50%'],
         radius=['30%', '75%'],
         rosetype='area',
         label_opts=opts.LabelOpts(is_show=True, formatter='价格区间{b}：共{c}个，占{d}%'),

     )
    .set_global_opts(
        legend_opts=opts.LegendOpts(is_show=True),
    )
)
data_pie.render_notebook()

amazon_kline = (
    chas.Kline()
    .add
)

