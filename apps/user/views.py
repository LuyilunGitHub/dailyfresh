from django.shortcuts import render

from django.views.generic import View  # 基于类的视图
from apps.user.models import User,Address  # 内部的User
from django.shortcuts import redirect  # 重定向
from django.core.urlresolvers import reverse
import re  # 正则
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer  # 加密
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate, login  # 登录
from celery_tasks.tasks import send_email  # 发送邮件

from utils.mixin import LoginRequiredMixin  # 重写as_view,没有登录有些页面不可以浏览
from django.contrib.auth import logout #退出

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse,JsonResponse

...


def send(request):
    msg = '<a href="http://www.jd.com" target="_blank">点击激活</a>'
    send_mail('注册激活', '', settings.EMAIL_FROM,
              ['422815634@qq.com'],
              html_message=msg)
    return HttpResponse('ok')


# 测试基于类的视图

# from django.views.generic.base import TemplateView
#
#
# class homeview(TemplateView):
#     template_name = "user/register.html"
#     def get_context_data(self, **kwargs):
#         context = super(homeview, self).get_context_data(**kwargs)
#         # context['latest_articles'] = Article.objects.all()[:5]
#         context['zhoujiekub']='zhoujiekub'
#         return context


# 测试注册
#
# from django.contrib.auth import authenticate
#
#
# class Register(TemplateView):
#     user = authenticate(username='john', password='secret')
#     if user is not None:
#         # the password verified for the user
#         if user.is_active:
#             print("User is valid, active and authenticated")
#         else:
#             print("The password is valid, but the account has been disabled!")
#     else:
#         # the authentication system was unable to verify the username and password
#         print("The username and password were incorrect.")


class Register(View):
    """用户注册"""

    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):
        username = request.POST.get('user_name', "")
        password = request.POST.get('pwd', "")
        email = request.POST.get('email', "")
        allow = request.POST.get("allow")
        if not all([username, password, email]):
            return render(request, "user/register.html", {"errage": "注册信息没有填写完整！"})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, "user/register.html", {"errage": "邮箱格式不正确！"})
        if allow is None:
            return render(request, "user/register.html", {"errage": "请同意协议！"})
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)
            user.is_active = 0;
            user.save()
            info = {'userId': user.id}
            serializer = Serializer(settings.SECRET_KEY, 3600).dumps(info)
            token = serializer.decode()
            send_email.delay(username, email, token)
            return render(request, "user/register.html", {"errage": "恭喜你，注册成功！，请前去邮箱激活"})
        else:
            return render(request, "user/register.html", {"errage": "注册的用户已经存在！"})


def isActive(request, token):
    serializer = Serializer(settings.SECRET_KEY, 3600).loads(token)
    try:
        userId = serializer['userId']
        user = User.objects.get(id=userId)
        user.is_active = 1
        user.save()
        return redirect(reverse('user:login'))
    except SignatureExpired as e:
        return HttpResponse('激活时间过时')


class Login(View):
    """登录"""

    def get(self, request):
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request, "user/login.html", {'username': username, 'checked': checked})

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("pwd")
        remember = request.POST.get("remember")
        if not all([username, password]):
            return render(request, "user/login.html", {"errage": "登录信息没有填写完整！"})
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', reverse('goods:index'))
                return redirect(next_url)

                if remember is None:
                    response.delete_cookie("username")
                else:
                    response.set_cookie("username", username, max_age=3600 * 24)
                return response
            else:
                return render(request, 'user/login.html', {'errage': '您的账号还没有激活,快到你邮箱激活吧！'})
        else:
            # the authentication system was unable to verify the username and password
            return render(request, 'user/login.html', {'errage': '对不起,你的用户名或密码输入错误！'})



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('user:login'))




class Cart(View):
    def get(self, request):
        return render(request, "user/cart.html")


class Detail(View):
    def get(self, request):
        return render(request, "user/detail.html")


class List(View):
    def get(self,request):
        return render(request, "user/list.html")


class Order(View):
    def get(self, request):
        return render(request, "user/place_order.html")


class CenOrder(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user/user_center_order.html",{'cenOrder':'active'})


class CenInfo(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "user/user_center_info.html",{'cenInfo':'active'})


class CenSite(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        is_default= request.GET.get("is_default","")
        print(is_default,"++++++++++++++++++++++++++++++++++++")
        # 更改默认地址
        if is_default:
            address = Address.newObject.get_default_addr(user)
            if address is not None:
                address.is_default = False
                address.save()
            defaultAddr = Address.newObject.get(id = int(is_default))
            defaultAddr.is_default = True
            defaultAddr.save()
            addrlist = Address.newObject.get_alladdrByuser(user)
            list = []
            for addrs in addrlist:
                list.append({"receiver":addrs.receiver,'addr':addrs.addr,'phone':addrs.phone,'is_default':addrs.is_default,'id':addrs.id})
            context={'addrlist':list}
            return JsonResponse(context)
        addrlist = Address.newObject.get_alladdrByuser(user)
        return render(request, "user/user_center_site.html",{'cenSite':'active','addrlist':addrlist})

    def post(self, request):
        phone=request.POST.get('phone')
        addr=request.POST.get('addr')
        receiver=request.POST.get('receiver')
        zip_code=request.POST.get('zip_code')
        if not all([phone,addr,receiver]):
            return render(request, "user/user_center_site.html", {'cenSite': 'active','errage':'信息没有填写完整'})
        if not re.match(r'^1[3|5|7|8]|\\d{9}$',phone):
            return render(request, "user/user_center_site.html", {'cenSite': 'active', 'errage': '手机格式不正确'})
        user=request.user
        address = Address.newObject.get_default_addr(user)
        is_default = False
        if address is None:
            is_default = True

        Address.newObject.create(user=user,phone=phone,addr=addr,receiver=receiver,zip_code=zip_code,is_default=is_default);
        addrlist = Address.newObject.get_alladdrByuser(user)
        return render(request, "user/user_center_site.html",{'cenSite':'active','addrlist':addrlist})

