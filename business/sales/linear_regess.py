from sklearn.linear_model import LinearRegression
from business.sales.base_regress import BaseRegress


# 线性回归
class LinearRegressionPredict(BaseRegress):
    def __init__(self, sheet_name="线性回归预测"):
        super().__init__(LinearRegression(), sheet_name)


if __name__ == '__main__':
    linear = LinearRegressionPredict()
    linear.predict("2024/1", "2024/6")
