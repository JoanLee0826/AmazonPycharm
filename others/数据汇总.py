import os
import pandas as pd
import datetime


def in_all(data_path):
    """
    合并Excel文件，在原路径下创建文件夹data/保存合并后的文件
    :param data_path: 许多Excel文件的路径
    :return:
    """
    df = pd.DataFrame()
    for each in os.listdir(data_path):
        if each.endswith('xlsx'):
            file = data_path + "/" + each
            df = pd.concat([df, pd.read_excel(file)], sort=False)
    aft = datetime.datetime.strftime(datetime.datetime.now(), '_%m%d_%H%M')
    out_path = data_path + '/data/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_file = out_path + '/合并' + aft + '.xlsx'
    df.to_excel(out_file)
    return "文件合并保存在目录：{}".format(os.path.realpath(out_path))


if __name__ == '__main__':
    data_path = r'E:\AmazonPycharm\data\临时合并'
    print(in_all(data_path))