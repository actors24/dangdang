import datetime
import random
import string
import hashlib   # sha 和 md5

from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from home.models import TBook
from user.captcha.image import ImageCaptcha
from user.models import TUser, TCart, TAddress, TOrder, TUserOrder


# 登录页面函数
def login(request):
    # 获取url，用于之后路径的回跳
    url = request.GET.get('url')
    if 'indent' in url:
        pass
    else:
        url = request.META.get('HTTP_REFERER')
        if 'login' in url or 'register' in url:
            url = request.session.get('url')
        request.session['url'] = url
    # 从cookies中获取用户名和密码跟数据库比对
    username = request.COOKIES.get('username')
    pwd = request.COOKIES.get('password')
    user = TUser.objects.filter(username=username)
    if user:
        # 用户数据比对成功，重定向到首页
        if TUser.objects.filter(username=username, password=pwd):
            request.session['flag'] = True
            return redirect('home:index')

    # 数据比对失败，渲染登录页面
    return render(request, 'login.html', {'url': url})


# 登录逻辑函数
def login_logic(request):
    try:
        # 获取登录页面中的用户名和密码
        username = request.POST.get('txtUsername')
        pwd = request.POST.get('txtPassword')
        rem = request.POST.get('autologin')
        # 用户名或者密码为空时登录失败
        if username == '' or pwd == '':
            return HttpResponse(0)
        # 用户名和加密后的密码与数据库做比对
        user = TUser.objects.get(username=username)
        sha = hashlib.sha1()
        sha.update((pwd+user.salt).encode())
        new_pwd = sha.hexdigest()
        user = TUser.objects.filter(username=username, password=new_pwd)
        # 用户名存在，进行登录程序
        if user:
            resp = HttpResponse(1)
            # 把用户名存入session中，以便登录后的使用
            request.session['username'] = username
            request.session['flag'] = True
            # 从session中获取未登录状态时的购物车
            cart = request.session.get('cart')
            # 根据用户名找到对应的用户对象
            user = TUser.objects.get(username=username)
            # 根据用户id找到对应的购物车数据
            books = TCart.objects.filter(user_id=user.pk)
            # 如果session中的购物车存在则把其中的数据叠加到用户的购物车
            if cart:
                # 把用户购物车和session购物车中的数据进行二次循环，如果对应的图书id相等则把session中对应的图书的数量叠加到用户购物车对应的图书上，然后保存数据
                for book1 in books:
                    for book2 in cart:
                        if book1.book_id == int(book2['id']):
                            book1.count += int(book2['num'])
                            book1.save()
                            # 从session中的购物车中移除该图书，保证session中的图书都是用户购物车中没有的
                            cart.remove(book2)
                            # 跳出内层循环
                            break
                # 把session中的购物车的不重复的图书循环加入到用户的购物车中
                for book in cart:
                    TCart.objects.create(book_id=book['id'], count=book['num'], user_id=user.pk)
                # 把session中的购物车数据删除
                del request.session['cart']
            # 勾选了7天自动登录
            if rem:
                # 设置flag用于自动登录的验证
                request.session['flag'] = True
                # 把当前用户名和密码存入cookies
                resp.set_cookie('username', username, max_age=7 * 24 * 3600)
                resp.set_cookie('password', new_pwd, max_age=7*24*3600)
            return resp
        return HttpResponse(0)
    # 遇到异常时，返回登录失败
    except:
        return HttpResponse(0)


# 注册页面函数
def register(request):
    # 获取url，用于之后路径的回跳
    url = request.GET.get('url')
    if 'indent' in url:
        pass
    else:
        url = request.META.get('HTTP_REFERER')
        if 'login' in url or 'register' in url:
            url = request.session.get('url')
        request.session['url'] = url
    # 渲染注册页面
    return render(request, 'register.html', {'url': url})


# 注册逻辑函数
def register_logic(request):
    # 获取注册页面的用户名密码，确认密码
    username = request.POST.get('txt_username')
    pwd = request.POST.get('txt_password')
    repwd = request.POST.get('txt_repassword')
    try:
        # 手动添加事务控制，保持事务的完整性
        with transaction.atomic():
            # 判断数据合法性，其中一项不合法则返回注册失败
            if username == '' or pwd == '' or repwd == '' or pwd != repwd:
                return HttpResponse(0)
            # 数据合法，进行数据库校验
            else:
                salt = str(random.randint(100000, 999999))
                sha = hashlib.sha1()
                sha.update((pwd+salt).encode())
                pwd = sha.hexdigest()
                user = TUser.objects.create(username=username, password=pwd, salt=salt)
                # 验证成功，保存session，返回注册成功
                if user:
                    request.session['username'] = username
                    # 从session中获取未登录状态时的购物车
                    cart = request.session.get('cart')
                    # 根据用户名找到对应的用户对象
                    user = TUser.objects.get(username=username)
                    # 根据用户id找到对应的购物车数据
                    books = TCart.objects.filter(user_id=user.pk)
                    # 如果session中的购物车存在则把其中的数据叠加到用户的购物车
                    if cart:
                        # 把用户购物车和session购物车中的数据进行二次循环，如果对应的图书id相等则把session中对应的图书的数量叠加到用户购物车对应的图书上，然后保存数据
                        for book1 in books:
                            for book2 in cart:
                                if book1.book_id == int(book2['id']):
                                    book1.count += int(book2['num'])
                                    book1.save()
                                    # 从session中的购物车中移除该图书，保证session中的图书都是用户购物车中没有的
                                    cart.remove(book2)
                                    # 跳出内层循环
                                    break
                        # 把session中的购物车的不重复的图书循环加入到用户的购物车中
                        for book in cart:
                            TCart.objects.create(book_id=book['id'], count=book['num'], user_id=user.pk)
                        # 把session中的购物车数据删除
                        del request.session['cart']
                    return HttpResponse(1)
    # 情况异常，返回注册失败
    except:
        return HttpResponse(0)


# 注册完成页面函数
def register_ok(request):
    # 获取url，用于之后路径的回跳
    url = request.GET.get('url', '/dangdang/index')
    # 从session中获取用户名，设置flag
    username = request.session.get('username')
    request.session['flag'] = True
    # 渲染注册成功页面
    return render(request, 'register ok.html', {'username': username, 'url': url})


# 验证码函数
def get_captcha(request):
    # 构造验证码对象
    img = ImageCaptcha()
    # 生成随机的字符，由数字和字母组成，最后生成一个长度为5位的列表
    code = random.sample(string.ascii_letters + string.digits, 5)
    # 将生成的列表构造成字符串
    code = ''.join(code)
    # 将生成的字符串存于session中，用于验证码的对比验证
    request.session['code'] = code
    # 将字符串打到图片中
    data = img.generate(code)
    # 返回最终的验证码图片，第二个参数表示数据的文件类型是图片类型
    return HttpResponse(data, 'image/png')


# 检查用户名函数
def check_username(request):
    # 获取url中的用户名
    username = request.GET.get('username')
    # 数据库中存在此用户名，返回用户名已存在
    if TUser.objects.filter(username=username):
        return HttpResponse(0)
    # 数据库中无此用户名
    return HttpResponse(1)


# 检查验证码函数
def check_captcha(request):
    # 从url中获取验证码
    code = request.GET.get('code')
    # 从session中获取存好的验证码
    code1 = request.session.get('code')
    # 如果两个验证码的小写对比相同则返回1
    if code.lower() == code1.lower():
        return HttpResponse(1)
    # 对比失败返回0
    else:
        return HttpResponse(0)


# 退出函数
def log_out(request):
    # 把session中的数据全部清空
    request.session.clear()
    # 从路径中获取url参数，用于退出时跳转到指定页面，如果没有此参数则加默认值，默认跳转到首页
    url = request.META.get('HTTP_REFERER')
    if 'indent' in url:
        url = '/dangdang/index'
    # 重定向到url参数指定的路径
    resp = redirect(url)
    # 如果cookies中存在用户名和密码，则把用户名和密码设为空字符，有效期为1秒，1秒后自动删除
    if request.COOKIES.get('username'):
        resp.delete_cookie('username')
        resp.delete_cookie('password')
    return resp


# 购物车页面函数
def cart(request):
    # 从session中获取用户名，没有则从cookies中获取
    username = request.session.get('username')
    # 如果用户名存在，则表示为登录状态
    if username:
        # # 从session中获取未登录状态时的购物车
        # cart = request.session.get('cart')
        # 根据用户名找到对应的用户对象
        user = TUser.objects.get(username=username)
        # # 根据用户id找到对应的购物车数据
        # books = TCart.objects.filter(user_id=user.pk)
        # # 如果session中的购物车存在则把其中的数据叠加到用户的购物车
        # if cart:
        #     # 把用户购物车和session购物车中的数据进行二次循环，如果对应的图书id相等则把session中对应的图书的数量叠加到用户购物车对应的图书上，然后保存数据
        #     for book1 in books:
        #         for book2 in cart:
        #             if book1.book_id == int(book2['id']):
        #                 book1.count += int(book2['num'])
        #                 book1.save()
        #                 # 从session中的购物车中移除该图书，保证session中的图书都是用户购物车中没有的
        #                 cart.remove(book2)
        #                 # 跳出内层循环
        #                 break
        #     # 把session中的购物车的不重复的图书循环加入到用户的购物车中
        #     for book in cart:
        #         TCart.objects.create(book_id=book['id'], count=book['num'], user_id=user.pk)
        #     # 把session中的购物车数据删除
        #     del request.session['cart']
        # 构造一个空的购物车列表
        cart = []
        # 把用户的购物车循环遍历
        # amount = 0
        for book in TCart.objects.filter(user=user.pk):
            # 构造一个空字典
            d1 = dict()
            # 往空字典中存图书的相关属性，用键值对的方式存储
            d1['id'] = TBook.objects.get(pk=book.book_id).pk
            d1['name'] = TBook.objects.get(pk=book.book_id).book_name
            d1['image'] = TBook.objects.get(pk=book.book_id).image
            d1['num'] = book.count
            d1['price'] = TBook.objects.get(pk=book.book_id).discount
            d1['sum_price'] = d1['num'] * d1['price']
            # amount += d1['num']
            # 往购物车列表追加一个字典，一个字典表示一个图书的信息
            cart.append(d1)
    # 用户名不存在，表示为未登录状态，从session中获取购物车数据，没有则默认赋值为空列表
    else:
        cart = request.session.get('cart', [])
    # 渲染购物车页面，把购物车数据通过传值的方式传送给前端
    return render(request, 'car.html', {'cart': cart, 'username': username})


# 加入购物车逻辑函数1
def cart_logic(request):
    try:
        with transaction.atomic():
            # 从session中获取用户名
            username = request.session.get('username', request.COOKIES.get('username'))
            # 获取书的id和数量
            book_id = request.GET.get('book_id')
            book_num = request.GET.get('book_num')
            # 登录状态时对数据库中的数据进行修改
            if username:
                # 根据用户名找到用户
                user = TUser.objects.get(username=username)
                # 根据用户id找到购物车
                books = TCart.objects.filter(user_id=user.pk)
                # 对购物车进行遍历
                for book in books:
                    # 如果此书已存在，则对数量进行叠加
                    if book.book_id == int(book_id):
                        book.count += int(book_num)
                        book.save()
                        break
                # 如果不存在，则添加新的图书
                else:
                    TCart.objects.create(book_id=book_id, count=book_num, user_id=user.pk)
                return HttpResponse(1)
            # 未登录状态修改session
            else:
                # 获取session中的购物车
                book_list = request.session.get('cart')
                # 如果购物车存在
                if book_list:
                    # 对购物车中的书遍历，如果此书已存在，则增加数量，再保存新的session
                    for book in book_list:
                        if book['id'] == book_id:
                            num = int(book['num'])
                            num += int(book_num)
                            book['num'] = num
                            request.session['cart'] = book_list
                            return HttpResponse(1)
                    # 如果是新的书则构造一个字典，这个字典表示新增加的图书
                    else:
                        book1 = TBook.objects.get(pk=book_id)
                        name = book1.book_name
                        image = book1.image
                        price = book1.discount
                        # 往原来的购物车列表追加一个字典
                        book_list.append({'id': book_id, 'name': name, 'image': image, 'price': price, 'num': book_num})
                        # 重新保存session
                        request.session['cart'] = book_list
                        return HttpResponse(1)
                # 如果购物车不存在
                else:
                    # 新建一个空列表
                    book_list = []
                    # 往列表添加一个字典
                    book1 = TBook.objects.get(pk=book_id)
                    name = book1.book_name
                    image = book1.image
                    price = book1.discount
                    book_list.append({'id': book_id, 'name': name, 'image': image, 'price': price, 'num': book_num})
                    # 保存session
                    request.session['cart'] = book_list
                    return HttpResponse(1)
    except:
        return HttpResponse(0)


# 修改购物车图书逻辑2
def cart_logic1(request):
    with transaction.atomic():
        username = request.session.get('username', request.COOKIES.get('username'))
        book_id = request.GET.get('book_id')
        book_num = request.GET.get('book_num')
        # 登录状态
        if username:
            user = TUser.objects.get(username=username)
            books = TCart.objects.filter(user_id=user.pk)
            # 当图书与库中的图书相同时，修改该书的数量并保存
            for book in books:
                if book.book_id == int(book_id):
                    book.count = int(book_num)
                    book.save()
                    break
        # 未登录状态
        else:
            # 从session中获取购物车
            book_list = request.session.get('cart')
            # 当图书与库中的图书相同时，修改该书的数量并保存
            for book in book_list:
                if book['id'] == book_id:
                    num = int(book['num'])
                    num = int(book_num)
                    book['num'] = num
                    # 把修改后的结果重新存入session
                    request.session['cart'] = book_list
        return HttpResponse(1)


# 删除购物车书籍逻辑函数3
def cart_logic2(request):
    with transaction.atomic():
        # 获取用户名和图书id
        username = request.session.get('username', request.COOKIES.get('username'))
        book_id = request.GET.get('book_id')
        # 登录状态时
        if username:
            # 从库中找到该本书并将他删除
            user = TUser.objects.get(username=username)
            books = TCart.objects.filter(user_id=user.pk)
            for book in books:
                if book.book_id == int(book_id):
                    book.delete()
                    break
        # 未登录状态
        else:
            # 从session获取购物车
            book_list = request.session.get('cart')
            # 找到该图书并将他删除
            for book in book_list:
                if book['id'] == book_id:
                    book_list.remove(book)
            # 重新保存session
            request.session['cart'] = book_list
        return HttpResponse(1)


# 订单页面函数
def indent(request):
    # 从session获取用户名并找到对应的地址和购物车
    username = request.session.get('username')
    if username:
        pass
    else:
        url = reverse('user:login')+'?url=/dangdang/indent'
        return redirect(url)
    user_id = TUser.objects.get(username=username).pk
    address = TAddress.objects.filter(user_id=user_id)
    cart = TCart.objects.filter(user_id=user_id)
    # 设置总价，初始化为0
    money = 0
    # 对该用户的购物车中的每一本书进行小计，然后加给总价
    for i in cart:
        money += float(TBook.objects.get(pk=i.book_id).discount) * float(i.count)
    # 总价保留两位小数
    money = '%.2f' % money
    # 构造一个空列表，用于保存字典
    book = []
    # 往字典里添加键值对，为每本书的相关属性和值
    for i in cart:
        d1 = dict()
        d1['id'] = TBook.objects.get(pk=i.book_id).pk
        d1['name'] = TBook.objects.get(pk=i.book_id).book_name
        d1['price'] = TBook.objects.get(pk=i.book_id).discount
        d1['count'] = i.count
        d1['sum'] = d1['price'] * d1['count']
        d1['save_price'] = TBook.objects.get(pk=i.book_id).save_price()
        # 对列表进行追加
        book.append(d1)
    # 渲染订单页面
    return render(request, 'indent.html', {'username': username, 'address': address, 'money': money, 'cart': book})


# 订单逻辑函数
def indent_logic(request):
    try:
        with transaction.atomic():
            # 获取session中的用户名和表单中地址的相关信息
            username = request.session.get('username', request.COOKIES.get('username'))
            add_id = request.POST.get('id')
            name = request.POST.get('name')
            address = request.POST.get('address')
            zip_code = request.POST.get('zip_code')
            phone_number1 = request.POST.get('telephone')
            phone_number2 = request.POST.get('home_phone')
            # 拿到库中地址表的所有id，然后与表单中的地址id进行比对
            user_id = TUser.objects.get(username=username).pk
            adds = list(TAddress.objects.all().values('id'))
            for add in adds:
                # 如果地址id相同，则表示是原先的地址，跳出循环
                if int(add_id) == add['id']:
                    break
            # 如果不相同，则往地址表中添加新的地址
            else:
                TAddress.objects.create(name=name, address=address, zip_code=zip_code, phone_number=phone_number1, home_number=phone_number2, user_id=user_id)
            return HttpResponse(1)
    except:
        return HttpResponse(0)


# 修改地址表函数
def address_ajax(request):

    def mydefault(a):
        if isinstance(a, TAddress):
            return {'id': a.pk, 'name': a.name, 'address': a.address, 'zip_code': a.zip_code, 'telephone': a.phone_number, 'home_phone': a.home_number}
    # 从url中获取地址id，并从库中查到该地址
    add_id = int(request.GET.get('address_id'))
    address = TAddress.objects.get(pk=add_id)
    # 返回json字符串
    return JsonResponse({'address': address}, json_dumps_params={'default': mydefault})


# 订单完成页面函数
def indent_ok(request):
    # 获取用户名
    username = request.session.get('username')
    # 从url总获取名字和地址id
    name = request.GET.get('name')
    add_id = request.GET.get('add_id')
    user_id = TUser.objects.get(username=username).pk
    # 对应用户的购物车
    cart = TCart.objects.filter(user_id=user_id)
    # 设置两个变量，amount表示该用户购物车图书的总数量，sum_price表示总价
    amount = 0
    sum_price = 0
    for i in cart:
        amount += i.count
        sum_price += TBook.objects.get(pk=i.book_id).discount * i.count
    # 总价保留两位小数
    sum_price = '%.2f' % sum_price
    # 随机生成一个订单号，是一个十位数字的字符串
    order_id = str(random.randint(1000000000, 9999999999))
    # 订单状态为1
    status = 1
    # 设置订单生成时间为标准时间
    create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 判断地址是新填写的还是原来库中的，如果是新的，则该订单对应的地址id为库中地址表最后一行数据的id
    if add_id == '0':
        address_id = TAddress.objects.last().pk
    # 如果是原来的地址，则地址id为获取到的地址id
    else:
        address_id = add_id
    # 往订单表添加一行数据
    TUserOrder.objects.create(order_id=order_id, amount=amount, user_id=user_id, status=status, create_time=create_time, price=sum_price, address_id=address_id)
    # 为对应的订单创建订单项表，表中包含订单表里含有的图书，与订单表相关联
    for i in cart:
        TOrder.objects.create(book_id=i.book_id, amount=i.count, order_id=TUserOrder.objects.last().pk)
    # 最后把该用户的购物车清空
    cart.delete()
    return render(request, 'indent ok.html', {'username': username, 'amount': amount, 'sum_price': sum_price, 'name': name, 'order_id': order_id})


# 发送邮件函数
def send_email(request):
    try:
        # 从url中获取目标邮件地址
        email = request.GET.get('email')
        # 发送邮件
        send_mail('hello', '你已成功注册！', '1361550064@qq.com', [email], fail_silently=False)
        return HttpResponse(1)
    except:
        return HttpResponse(0)
