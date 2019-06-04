#### 本例说明如何使用django-rest-framework及vue实现前后端分离
#### 环境
* os mac
* Django 1.11.20
* Redis v=5.0.3
* django-redis 4.10.0
* djangorestframework 3.5.4
* Celery 4.3.0
* celery-redbeat 0.13.0
* vue 2.9.3
* node v8.11.1
* npm 5.6.0
#### 内容包括
* 认证(包括自定义认证后端)
* 权限(包括自定义权限管理)
* 限流(包括自定义限流策略;针对匿名用户,登录用户及VIP用户有不同的阈值)
* django-redis作为缓存后端
* 基于django-rest-framework的token认证
* 登录登出
* 基于视图的权限管理
* 信号使用（可以控制在请求开始前后完成后执行一些逻辑）
* 扩展manage.py实现自定义management command
* 自定义中间件
* 基于celery的异步任务及定时任务
#### 部分说明
* schema_view 返回api接口文档
* 创建virtualenv,并激活
* 执行项目根目录下的start,启动服务
* 创建管理员,在项目根目录执行`python manage.py createsuperuser`并根据提示输入相关信息
* 然后可以用管理员用户登录管理页(http://localhost:9000/admin/)进行用户的管理
* 申请token，post请求（http://localhost:9000/gentoken/）即可
    实例：
    ```
    请求：
    import requests
    data = {'username':'user3','password':'123456'}
    res = requests.post('http://localhost:9000/gentoken/',json=data)
    返回：
    res.json()
    {u'token': u'89c27c3dbb497b911e571eea387e0b0fc771d369'}
    ```
* 基于token认证的api请求实例
    ```
    请求：
    import requests
    headers = {'Authorization': 'Token f165baa8ee7d23f48289aed29579c25cbd8e3247'}
    res = requests.get('http://localhost:9000/vue/',headers=headers)
    返回：
    res.json()
    {u'errno': u'0', u'data': u'ok'}
    ```
#### celery使用说明
1. 在restpro/restpro下新增celery.py （defines the Celery instance）
2. 在restpro/restpro下的__init__.py中import this app（This ensures that the app is loaded when Django starts so that the @shared_task decorator (mentioned later) will use it）
3. 在restpro/restpro下的settings.py中增加celery相关的配置,**注意CELERY_TIMEZONE = TIME_ZONE**
4. 在应用（restpro/restapp）下增加tasks.py在其中添加异步任务及定时任务;**注意:tasks.py必须在各app根目录下且名字必须是tasks.py**
5. 测试异步任务
    1. 进入Django shell:`python manage.py shell --setting=restpro.settings`
    2. 导入异步任务: `from restapp.tasks import *`
    3. 调用异步任务: `res = add.delay(3,4)`
    4. 获取异步任务结果: `res.get()`，获取成功则测试通过
6. 测试定时任务
    1. 在一个窗口启动celery worker: `celery worker -A restpro -Q default,custom`
    2. 在另一个窗口启动celery beat: `celery -A restpro beat -l info`
    3. 观察两个窗口的输出，如果beat窗口有发送任务且worker窗口有结果输出，则测试通过
7. 启动celery worker及beat,详见`celery-worker-start.sh`
8. celery beat使用celery-redbeat scheduler
   ##### 原因:
   由于celery自带的scheduler(celery.beat.PersistentScheduler)及[jango-celery-beat 1.5.0](https://github.com/celery/django-celery-beat)都不支持多实例部署，如果多实例启动beat的话，任务将被重复调度，因此没法实现高可用，要实现高可用需要使用第三方调度，比如:
   1. [redbeat 0.13.0](https://github.com/sibson/redbeat):
   虽然支持多机部署,且不会重复调度,但是当前生效的调度器挂了以后,其他存活的调度器接管其调度的任务会有延迟,可能会导致任务少执行几次,但是能够实现高可用且定时任务少执行几次可接受,因此选择使用此调度器
   2. [celery-redundant-scheduler 0.0.1](https://github.com/MnogoByte/celery-redundant-scheduler):
   测试发现,无法正常调度任务,放弃使用
   ##### 使用方法:
   1. 安装: `pip install celery-redbeat`
   2. 修改配置: 在settings.py中增加REDBEAT_REDIS_URL,并设置CELERYBEAT_MAX_LOOP_INTERVAL = 30(默认300),以减小延迟时间,redbeat_lock_timeout = 5 * CELERYBEAT_MAX_LOOP_INTERVAL
   3. 使用-S redbeat.RedBeatScheduler启动celery beat: `celery -A restpro beat -l info -S redbeat.RedBeatScheduler`

#### 相关链接
1. [django源码](https://github.com/django/django)
2. [django文档](https://docs.djangoproject.com/zh-hans)
3. [django-rest-framework源码](https://github.com/encode/django-rest-framework)
4. [django-rest-framework文档](https://q1mi.github.io/Django-REST-framework-documentation)
5. [celery-4.3文档](http://docs.celeryproject.org/en/latest/index.html)
6. [celery-redbeat文档](https://pypi.org/project/celery-redbeat/)
