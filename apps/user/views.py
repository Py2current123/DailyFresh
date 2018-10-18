from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import View
from user.models import User
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import re

# Create your views here.

class RegisterView(View):
    '''用户注册类'''

    def get(self, request):
        '''显示用户注册页面'''

        return render(request, 'register.html')

    def post(self, request):
        '''注册处理'''

        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        again_password = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # print(allow)
        # print(type(password))


        # 数据校验
        if not all([username, password, again_password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})


        # 校验二次输入的密码是否一致
        if password != again_password:
            return render(request, "register.html", {'errmsg': '二次密码输入的不一致'})

        # 校验邮箱地址合法性
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱地址不合法'})

        # 校验用户是否同意协议
        # if allow != 'on':
        if allow == None:
            return render(request, 'register.html', {'errmsg': '请先同意协议'})

        # 注册用户信息写入数据库
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 发送激活邮件，包含激活链接: http://127.0.0.1:8000/user/active/3
        # 激活链接中需要包含用户的身份信息, 并且要把身份信息进行加密

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        # 发送邮件,用celery实现异步，提高用户体验
        send_register_active_email.delay(email, username, token)

        # 返回应答，跳转到首页
        return redirect(reverse('goods:index'))
















