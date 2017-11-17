
from django.conf.urls import  url
from apps.user import views
from django.contrib.auth.decorators import login_required
urlpatterns = [

    url(r'^send$',views.send),
    url(r'^register',views.Register.as_view(),name='register'),
    url(r'^isActive(?P<token>.*)',views.isActive,name='isActive'),
    # url(r'^',views.Index.as_view(),name='index'),
    url(r'^login',views.Login.as_view(),name='login'),
    #退出
    url(r'^logout', views.Logout.as_view(), name='logout'),




    url(r'^cart', views.Cart.as_view(), name='cart'),
    url(r'^detail', views.Detail.as_view(), name='detail'),
    url(r'^list', views.List.as_view(), name='list'),
    url(r'^order', views.Order.as_view(), name='order'),
    url(r'^cenInfo', views.CenInfo.as_view(), name='cenInfo'),
    url(r'^cenOrder', views.CenOrder.as_view(), name='cenOrder'),
    url(r'^cenSite', views.CenSite.as_view(), name='cenSite'),


]
