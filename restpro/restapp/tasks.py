# -*- coding: utf-8 -*-
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

#如果bind=True,那么task的第一个参数为self
@shared_task(bind=True, queue='default', soft_time_limit=300)
def add(self, x, y):
    return x + y


@shared_task(queue='default', soft_time_limit=300)
def add_nobind(x, y):
    return x + y


@shared_task(bind=True, queue='custom', soft_time_limit=300)
def mul(slef, x, y):
    return x * y


@shared_task(bind=True, queue='custom', soft_time_limit=300, ignore_result=True)
def xsum(self, numbers):
    return sum(numbers)


@shared_task(bind=True, queue='custom', soft_time_limit=300)
def cron1(self, arg1, arg2):
    # 这里调用django的management命令，可以是内置的也可以是扩展的，比如这里调用扩展的命令extent_manage_example
    from django.core.management import call_command
    call_command('extent_manage_example')
    print('arg1:', arg1)
    print('arg2:', arg2)

@shared_task(queue='default', soft_time_limit=300)
def cron2():
    print('this is restapp cron2')
