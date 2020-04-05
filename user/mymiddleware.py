from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from user.models import TUser


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("init1")

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        # 如果以下某一字符串包含在了路径中，检查登录状态
        if "index" in request.path or "book_list" in request.path or "book_detail" in request.path or "cart" in \
                request.path:
            # flag为True，则表示此时为持续会话状态，不做任何事
            if request.session.get('flag'):
                pass
            else:
                # flag为False，表示创建会话，则拿到浏览器中的cookies，跟数据库做比对，如果比对成功，则表示免登录，设置flag为True,在session中保存用户名
                username = request.COOKIES.get('username')
                password = request.COOKIES.get('password')
                user = TUser.objects.filter(username=username, password=password)
                if user:
                    request.session['flag'] = True
                    request.session['username'] = username
                else:
                    # 数据匹配不成功，设置用户名为空字符串
                    request.session['username'] = ''
        else:
            pass
        # 如果以下字符串包含在路径中，则判断他是由哪个页面跳转过来的
        if 'indent' in request.path or 'indent_ok' in request.path:
            # 前置页面存在，则不做任何事情
            if request.META.get('HTTP_REFERER'):
                pass
            # 如果前置页面为空，则表示是直接输入url跳转地址的，此时一律跳回首页
            else:
                return redirect('home:index')



    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("view:", request, view_func, view_args, view_kwargs)

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        print("response:", request, response)
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        print("exception:", request, ex)
        # return redirect("user:login")