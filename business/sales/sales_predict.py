from business.sales.base_regress import write_data
from business.sales.linear_regess import LinearRegressionPredict
from business.sales.multiple_linear_regress import LinearRegressionPoly
from business.sales.random_forest_regress import RandomForest
from business.sales.ridge_regress import ElasticNetRegression
from business.sales.svr import SVRegress


def predict(method: str, start: str, end: str):
    model = None
    if method == "线性回归":
        model = LinearRegressionPredict()
    elif method == "多元线性回归":
        model = LinearRegressionPoly(3)
    elif method == "随机森林回归":
        model = RandomForest()
    elif method == "弹性网络回归":
        model = ElasticNetRegression()
    elif method == "支持向量机回归":
        model = SVRegress()
    elif method == "循环神经网络":
        model = LinearRegressionPredict()

    data, res_dict = model.predict(start, end)
    write_data(data, method, start, end)
    return res_dict


if __name__ == '__main__':
    res = predict("线性回归", "2024/2", "2024/10")
    print(res)
