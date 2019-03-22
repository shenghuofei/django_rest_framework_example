#### 本例说明如何使用django-rest-framework
#### 环境
* os mac
* Django 1.11.20
* django-redis 4.10.0
* djangorestframework 3.5.4
#### 内容包括
* 认证(包括自定义认证后端)
* 权限(包括自定义权限管理)
* 限流(包括自定义限流策略;针对匿名用户,登录用户及VIP用户有不同的阈值)
* django-redis作为缓存后端
* 基于django-rest-framework的token认证
* 登录登出
* 基于视图的权限管理
* 信号使用（可以控制在请求开始前后完成后执行一些逻辑）
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
