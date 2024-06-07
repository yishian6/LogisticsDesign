import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from utils.config_utils import BASE_DIR

month_factor = [1.038818159, 0.725013207, 1.131863506, 0.794702366, 1.098858928, 1.143396069, 0.918415849, 0.924550492,
                1.107411921, 1.000931436, 0.9640458, 1.151992269]


# 机器学习的父类
class BaseRegress:
    def __init__(self, model, sheet_name="线性回归预测"):
        self.model = model
        # 输入数据
        file_path = os.path.join(BASE_DIR, 'business/sales/一汽数据处理.xlsx')
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        time_list = df['时间'].tolist()
        time_id_list = df['时间编号'].tolist()
        y_data = df['月份分离后的序列'].tolist()
        x_data = np.array(time_id_list)
        # 将x_data转换为二维数组
        x_data = x_data.reshape(-1, 1)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x_data, y_data, test_size=0.3,
                                                                                random_state=42)
        # 获取最后一个数据
        self.last_date = str(time_list[-1])
        self.last_time_id = time_id_list[-1]
        # 进行模型训练
        self.model.fit(self.x_train, self.y_train)

    def predict(self, start_time: str, end_time: str):
        """
        :param start_time: 预测的开始时间
        :param end_time: 预测的结束时间
        :return: 预测结果包含时间，时间编号，预测结果
        """
        start_id = handle_date(self.last_date, self.last_time_id, start_time)
        end_id = handle_date(self.last_date, self.last_time_id, end_time)
        data_list = get_date_list(start_time, end_time)
        x_predict = np.array([i for i in range(int(start_id), int(end_id) + 1)])
        x_predict = x_predict.reshape(-1, 1)
        y_pred = self.model.predict(x_predict)

        data = []
        final_regress = []
        for i in range(len(data_list)):
            final_regress.append(month_factor[int(data_list[i].split('/')[1]) - 1] * y_pred[i])
        for i in range(len(data_list)):
            data.append({
                "时间": data_list[i],
                "时间编号": int(x_predict[i]),
                "预测结果": y_pred[i],
                "最终结果": final_regress[i]
            })
        # print(data)
        res_dict = {"time": data_list, "result": final_regress}
        return data, res_dict


def handle_date(current_time, time_id, start: str):
    """
    :param current_time: 当前时间
    :param time_id: 当前时间编号
    :param start: 预测开始时间
    :return: 返回预测时间的时间编号
    """
    # 根据当前时间计算时间编号
    current_time_date = current_time.split("-")
    current_year = int(current_time_date[0])
    current_month = int(current_time_date[1])
    start_date = start.split("/")
    start_year = int(start_date[0])
    start_month = int(start_date[1])
    start_id = time_id + (start_year - current_year) * 12 + start_month - current_month
    return start_id


def get_date_list(start: str, end: str):
    """
    :param start: 预测的开始时间
    :param end: 预测的结束时间
    :return: 返回从开始时间到结束时间的时间编号
    """
    # 生成日期列表
    date_list = []
    start_date = start.split("/")
    start_year = int(start_date[0])
    start_month = int(start_date[1])
    end_date = end.split("/")
    end_year = int(end_date[0])
    end_month = int(end_date[1])
    for year in range(start_year, end_year + 1):
        if start_year == end_year:
            for month in range(start_month, end_month + 1):
                date_list.append(f"{year}/{month}")
        elif year == end_year:
            for month in range(1, end_month + 1):
                date_list.append(f"{year}/{month}")
        else:
            for month in range(start_month, 13):
                date_list.append(f"{year}/{month}")
    return date_list


# 将运费和时间写入文件
def write_data(d: list, method: str, start: str, end: str):
    """
    写入距离信息
    """
    start = start.replace("/", "-")
    end = end.replace("/", "-")
    write_file_path = os.path.join(BASE_DIR, f'data/prediction/{method}预测{start}~{end}.xlsx')
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(d)
    # 指定字段顺序
    order = ['时间', "时间编号", "预测结果", "最终结果"]
    pf = pf[order]
    # 替换空单元格
    pf.fillna(' ', inplace=True)

    # 输出到 Excel 文件
    with pd.ExcelWriter(write_file_path) as writer:
        # 输出到指定 sheet
        pf.to_excel(writer, index=False)

    # # 提示输出成功
    # print('成功输出省份距离到 Excel 文件！')
