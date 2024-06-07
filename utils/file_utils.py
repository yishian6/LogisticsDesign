import hashlib
import os

from utils.config_utils import FILE_SYSTEM_URL
from utils.log_utils import Logging
from abc import ABC, abstractmethod

log = Logging().get_logger()


class FSStorage(ABC):

    @staticmethod
    @abstractmethod
    def generate_filename(username):
        """生成文件名"""
        pass

    @staticmethod
    @abstractmethod
    def upload(username, user_uploaded_data):
        """上传文件"""
        pass

    @staticmethod
    @abstractmethod
    def get_local_path(filename):
        """获取文件路径"""
        pass

    @staticmethod
    @abstractmethod
    def is_file_exist(filename):
        """查看文件否存在，存在返回True"""
        pass


class AvatarStorage(FSStorage):
    @staticmethod
    def generate_filename(username):
        """生成头像文件名"""
        # 使用SHA256算法计算用户名的哈希值
        hash_object = hashlib.sha256(username.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        # 将哈希值作为文件名的一部分
        filename = 'avatar_' + hex_dig[:10] + '.png'
        return filename

    @staticmethod
    def upload(avatar_file, avatar_local_path):
        """上传头像文件"""
        avatar_file.save(avatar_local_path)

    @staticmethod
    def get_local_path(filename):
        """获取文件路径"""
        return os.path.join(FILE_SYSTEM_URL, AvatarStorage.__name__, filename)

    @staticmethod
    def is_file_exist(filename):
        """查看是否存在，存在返回True"""
        file_path = os.path.join(FILE_SYSTEM_URL, filename)
        return os.path.isfile(file_path)
