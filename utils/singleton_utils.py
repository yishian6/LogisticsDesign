# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/6/3
@Description: 装饰器实现单例
"""
import functools


def singleton(my_class):
    """
    装饰器实现单例模式，用法在单例类上加上@singleton即可
    :param my_class: 继承类
    :return: 单例对象
    """
    my_class.__new_original__ = my_class.__new__

    @functools.wraps(my_class.__new__)
    def singleton_new(a_class, *args, **kwargs):
        iterator = a_class.__dict__.get('__it__')
        if iterator is not None:
            return iterator
        iterator = a_class.__new_original__(a_class, *args, **kwargs)
        a_class.__it__ = iterator
        iterator.__init__original__(*args, **kwargs)
        return iterator

    my_class.__new__ = singleton_new
    my_class.__init__original__ = my_class.__init__
    my_class.__init__ = object.__init__
    return my_class
