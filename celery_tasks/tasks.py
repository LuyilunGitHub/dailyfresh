from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
import time
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
app=Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/6')
django.setup()

@app.task
def send_email(username,email,token):

    # 发送邮箱
    msg = '<h2>%s,就差一部就可以成为天天生鲜的会员了,点击下面链接，进行激活，赶快行动吧！</h2><br><a href="http://127.0.0.1:8000/user/isActive%s">%s</a>' % (
    username, token, token)
    send_mail('欢迎加入天天生鲜会员（会员验证）', '', settings.EMAIL_FROM, [email],html_message=msg)
    time.sleep(5)