from django.urls import path


from home import views

app_name = 'home'


urlpatterns = [
   path('index/', views.index, name='index'),  # 首页url
   path('book_detail/', views.bookdetail, name='book_detail'),  # 图书详情url
   path('book_list/', views.book_list, name='book_list'),  # 图书列表url
]
