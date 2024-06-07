from sklearn.ensemble import RandomForestRegressor
from business.sales.base_regress import BaseRegress


# 随机森林回归
class RandomForest(BaseRegress):
    def __init__(self, n_estimators=150, max_depth=4, random_state=42, sheet_name="随机森林回归预测"):
        # 创建线性回归模型对象
        super().__init__(
            RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state),
            sheet_name)


if __name__ == '__main__':
    rf = RandomForest()
    # 预测训练集和测试集
    rf.predict()
