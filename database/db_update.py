import pandas as pd
from utils.log_utils import Logging
# from database.db_init import column_names_news, column_names_job
# from sqlalchemy import desc
# from database.models import LastMile, RuralRevitalization, LogisticsPosition
# from utils.config_utils import BASE_DIR
# from common.base_exception import RenameFileException, DBUpdateException
# import os
# import shutil
# import datetime
#
# log = Logging().get_logger()
# data_current_path = os.path.join(BASE_DIR, 'data', 'current')
# data_finish_path = os.path.join(BASE_DIR, 'data', 'finished')
#
#
# def rename_file(file_path):
#     try:
#         now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#         filename, ext = os.path.splitext(os.path.basename(file_path))
#         new_filename = f'{filename}_{now_time}{ext}'
#         new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
#         # 拼接新的文件路径
#         os.rename(file_path, new_file_path)
#     except Exception:
#         raise RenameFileException
#
#
# def update_to_sql(excel_path, column_names, sql_table):
#     """
#     根据基于时间戳的增量更新
#     :param excel_path: excel路径
#     :param column_names: 中英标题名的字典
#     :param sql_table: 数据表模型
#     :return: None
#     """
#     try:
#         data = pd.read_excel(excel_path, engine='openpyxl')
#         data = data.rename(columns=column_names)
#         data_dict = data.to_dict(orient='records')
#         time_query = sql_table.query(sql_table.publish_date, order_by=desc(sql_table.publish_date), query_first=True)
#         data_list = []
#         for item in data_dict:
#             # 使用 pd.to_datetime() 方法将字符串转换为 Timestamp 类型
#             item['publish_date'] = pd.to_datetime(item['publish_date'])
#
#             # 筛选符合时间条件的数据并调用 sql_table() 函数进行处理
#             if item['publish_date'] > pd.Timestamp(time_query[0]):
#                 data_list.append(sql_table(**item))
#         sql_table.batch_add(data_list)
#
#         # 移动已处理完的文件到另一个文件夹中
#         shutil.move(excel_path, data_finish_path)
#         try:
#             rename_file(os.path.join(data_finish_path, os.path.basename(excel_path)))
#         except RenameFileException as e:
#             log.warning(str(e))
#         log.info(f'{sql_table.__tablename__} [{len(data_list)}] pieces of data were successfully updated')
#     except Exception:
#         raise DBUpdateException
#
#
# def data_update():
#     """
#     遍历指定文件夹下所有 Excel 文件，更新后移动文件
#     :return: None
#     """
#     if not os.path.exists(data_current_path):
#         log.warning('No File')
#     try:
#         for file_name in os.listdir(data_current_path):
#             if file_name.endswith('.xlsx'):
#                 file_path = os.path.join(data_current_path, file_name)
#                 if '乡村振兴' in file_path:
#                     update_to_sql(file_path, column_names_news, LastMile)
#                 elif '岗位信息' in file_path:
#                     update_to_sql(file_path, column_names_job, LogisticsPosition)
#                 elif '物流最后一公里' in file_path:
#                     update_to_sql(file_path, column_names_news, RuralRevitalization)
#     except DBUpdateException as e:
#         log.warning(str(e))
#
#
# def db_reconnection():
#     LastMile.query(LastMile.id, filter=[LastMile.id == 1], query_first=True)


# if __name__ == "__main__":
#     data_update()
