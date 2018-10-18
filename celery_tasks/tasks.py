# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

# 在任务处理者一端加这几句
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh_test.settings")
# django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://172.16.179.130:6379/8')












