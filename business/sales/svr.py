from sklearn.svm import SVR
from business.sales.base_regress import BaseRegress


class SVRegress(BaseRegress):
    def __init__(self, kernel='rbf', C=10, gamma=0.1, epsilon=0.2):  # kernel为核函数类型，C为正则化参数，epsilon为控制拟合误差的参数
        super(SVRegress, self).__init__(SVR(kernel=kernel, C=C, gamma=gamma, epsilon=epsilon), "支持向量机预测")


if __name__ == '__main__':
    svr = SVRegress()
    # 预测全部数据的
    pred, data_list = svr.predict()
