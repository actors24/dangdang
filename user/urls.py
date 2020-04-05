from django.urls import path

from user import views

app_name = 'user'


urlpatterns = [
    path('login/', views.login, name='login'),  # 登录页面url
    path('register/', views.register, name='register'),  # 注册页面url
    path('login_logic/', views.login_logic, name='login_logic'),  # 登录逻辑url
    path('register_logic/', views.register_logic, name='register_logic'),  # 注册逻辑url
    path('get_captcha/', views.get_captcha, name='get_captcha'),  # 验证码url
    path('check_username/', views.check_username, name='check_username'),  # 检查用户名url
    path('check_captcha/', views.check_captcha, name='check_captcha'),  # 检查验证码url
    path('register_ok/', views.register_ok, name='register_ok'),  # 注册成功页面url
    path('log_out/', views.log_out, name='log_out'),  # 退出url
    path('cart/', views.cart, name='cart'),  # 购物车页面url
    path('cart_logic/', views.cart_logic, name='cart_logic'),  # 添加购物车逻辑url
    path('cart_logic1/', views.cart_logic1, name='cart_logic1'),  # 购物车页面改变数量逻辑url
    path('cart_logic2/', views.cart_logic2, name='cart_logic2'),  # 购物车页面删除书籍url
    path('indent/', views.indent, name='indent'),  # 订单页面url
    path('indent_logic/', views.indent_logic, name='indent_logic'),  # 处理订单url
    path('address_ajax/', views.address_ajax, name='address_ajax'),  # 切换地址url
    path('indent_ok/', views.indent_ok, name='indent_ok'),  # 订单完成页面url
    path('mail/', views.send_email, name='mail'),  # 发送邮件url
]
