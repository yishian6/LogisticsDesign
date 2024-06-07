from sklearn.linear_model import ElasticNet

from business.sales.base_regress import BaseRegress


# 弹性网络回归
class ElasticNetRegression(BaseRegress):
    def __init__(self, alpha=0.1, l1_ratio=0.5):
        # alpha为正则化参数，l1_ratio为L1正则化项在正则化中所占的比例
        super().__init__(ElasticNet(alpha=alpha, l1_ratio=l1_ratio), "弹性网络回归预测")
        # # 创建并拟合弹性网络回归模型
        # self.model.fit(x_data, y_data)


if __name__ == '__main__':
    elastic = ElasticNetRegression()
    data_list = elastic.predict()
