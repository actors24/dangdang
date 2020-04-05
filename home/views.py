from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.


from home.models import TCategory,TBook


# 首页函数
def index(request):
    # 从session中获取用户名
    username = request.session.get('username', request.COOKIES.get('username'))
    # 把库中所有的一级分类，二级分类找出来
    cate1 = TCategory.objects.filter(level=1)
    cate2 = TCategory.objects.filter(level=2)
    # 获取出版时间最新的8本书
    book1 = TBook.objects.all().order_by('-publish_time')[0:8]
    # 获取一定时间内销量最高的5本书
    book2 = TBook.objects.all().filter(publish_time__gte='2019-12-24').order_by('-sale')[0:5]
    # 获取销量最高的8本书
    book3 = TBook.objects.all().order_by('-price')[0:8]
    # 渲染首页面
    return render(request, 'index.html', {'cate1': cate1, 'cate2': cate2, 'book1': book1, 'book2': book2, 'book3': book3, 'username': username})


# 图书详情函数
def bookdetail(request):
    # 从session中获取用户名
    username = request.session.get('username', request.COOKIES.get('username'))
    # 获取图书id
    book_id = int(request.GET.get('book_id', 1))
    # 根据id获取到对应的书籍
    book = TBook.objects.filter(id=book_id)
    # 获取该书对应的分类等级
    level = TCategory.objects.get(pk=book[0].category.pk).level
    # 如果等级为1，则找到该图书的一级分类名
    if level == 1:
        cate1 = TCategory.objects.get(pk=book[0].category.pk).category_name
        parent_id = book[0].category.pk
        return render(request, 'Book details.html', {'book': book, 'cate1': cate1, 'level': level, 'parent_id': parent_id, 'username': username})
    # 如果等级为2，则找到对应的一级分类的名字和二级分类名
    elif level == 2:
        children = TCategory.objects.get(id=book[0].category.id)
        children_id = children.pk
        parent_id = children.parent_id
        cate2 = children.category_name
        cate1 = TCategory.objects.filter(id=parent_id)[0].category_name
        return render(request, 'Book details.html', {'book': book, 'cate1': cate1, 'cate2': cate2, 'level': level, 'children_id': children_id, 'parent_id': parent_id, 'username': username})


# 图书列表函数
def book_list(request):
    # 获取用户名
    username = request.session.get('username', request.COOKIES.get('username'))
    # 从库中筛选所有的一级分类和二级分类
    cate1 = TCategory.objects.filter(level=1)
    cate2 = TCategory.objects.filter(level=2)
    # 从url中获取分类id和分类等级以及排序和页数
    cate_id = request.GET.get('category_id', 1)
    level = request.GET.get('level', 1)
    order = request.GET.get('order', '1')
    num = int(request.GET.get('num', 1))
    # 分类等级为1
    if int(level) == 1:
        # 构造一个空的queryset对象
        books = TBook.objects.filter(pk=-1)
        # 获取该一级分类对应的二级分类
        children = TCategory.objects.filter(parent_id=cate_id)
        # 获取该一级分类的名字
        parent_name = TCategory.objects.get(pk=cate_id).category_name
        # 遍历出每个二级分类对应的书籍，组成一个queryset对象
        for i in children:
            book = TBook.objects.filter(category=i.pk)
            books = books | book
        # 把该一级分类对应的图书加入到books这个queryset对象中
        books = books | TBook.objects.filter(category=cate_id)
        # 如果排序是1，则按默认排序
        if order == '1':
            pagnor = Paginator(books, per_page=4)
        # 如果排序是2，则按销量由高到低排序
        elif order == '2':
            pagnor = Paginator(books.order_by('-sale'), per_page=4)
        # 如果排序是3，则按价格从低到高排序
        elif order == '3':
            pagnor = Paginator(books.order_by('price'), per_page=4)
        # 如果排序是4， 则按出版时间由近到远排序
        elif order == '4':
            pagnor = Paginator(books.order_by('-publish_time'), per_page=4)
        # 如果页数不在范围的话，则跳转到第一页
        if int(num) not in pagnor.page_range:
            num = 1
        # 构造当前页对象
        page = pagnor.page(num)
        # 渲染图书列表
        return render(request, 'booklist.html',
                      {'page': page, 'category_id': cate_id, 'level': level, 'cate1': cate1, 'cate2': cate2,'parent_name': parent_name, 'username': username, 'order': order})
    # 分类等级为2
    elif int(level) == 2:
        if order == '1':
            books = TBook.objects.filter(category=cate_id)
        elif order == '2':
            books = TBook.objects.filter(category=cate_id).order_by('-sale')
        elif order == '3':
            books = TBook.objects.filter(category=cate_id).order_by('price')
        elif order == '4':
            books = TBook.objects.filter(category=cate_id).order_by('-publish_time')
        # 获取到该二级分类对应的一级分类名和二级分类名
        children = TCategory.objects.get(id=cate_id)
        children_name = children.category_name
        parent_id = children.parent_id
        parent_name = TCategory.objects.get(id=parent_id).category_name
        pagnor = Paginator(books, per_page=4)
        if int(num) not in pagnor.page_range:
            num = 1
        page = pagnor.page(num)
        return render(request, 'booklist.html', {'page': page, 'category_id': cate_id, 'parent_id':parent_id, 'level': level, 'cate1': cate1, 'cate2': cate2, 'parent_name': parent_name, 'children_name': children_name, 'username': username, 'order': order})
