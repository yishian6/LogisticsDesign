import time
from database.models import RegressPredict as RP
# 打印当前时间
operates = f"使用多元线性回归预测2023/12~2024/10的汽车销量情况"
rp_add = RP(operate=operates, create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
rp_add.add()