from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

from business.sales.base_regress import BaseRegress


# 多元线性回归
class LinearRegressionPoly(BaseRegress):
    def __init__(self, degree):
        self.degree = degree
        super().__init__(LinearRegression(), "多元线性回归预测")
        poly_features = PolynomialFeatures(degree=self.degree, include_bias=False)
        # x_poly = poly_features.fit_transform(x_train)
        # 创建一个包含多项式特征转换和线性回归的pipeline
        self.model = make_pipeline(poly_features, self.model)
        # 拟合模型
        self.model.fit(self.x_train, self.y_train)


if __name__ == '__main__':
    poly = LinearRegressionPoly(3)
    # 预测全部数据的
    pred, write_data = poly.predict()
