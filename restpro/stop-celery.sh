ps aux|grep -v grep |grep celery|awk '{print $2}'|xargs kill -9
