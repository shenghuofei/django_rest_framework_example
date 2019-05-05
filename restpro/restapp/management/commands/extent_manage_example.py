# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from django.core.management.base import BaseCommand, CommandError

'''
实现方法：
1.在app目录下创建management/commands目录,并在management和commands下面新建__init__.py使其作为模块
2.在commands下新增自定义命令文件，文件名即为命令名
3.自定义命令需要定义Command类并实现handle方法
'''

def this_is_other_task():
    print("can call other method")

class Command(BaseCommand):
    # 必须实现handle方法，调用时将执行handle方法
    def handle(self, *args, **kwargs):
        try:
            print("this is a extent manage command example")
            this_is_other_task()
        except Exception:
            raise CommandError("extent_manage_example error")
