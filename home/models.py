from django.db import models

# Create your models here.


class TBook(models.Model):
    book_name = models.CharField(max_length=20, blank=True, null=True)  # 书名
    author = models.CharField(max_length=20, blank=True, null=True)  # 作者
    org = models.CharField(max_length=20, blank=True, null=True)  # 出版社
    publish_time = models.DateField(blank=True, null=True)  # 出版时间
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # 价格
    discount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  # 折扣价
    comment = models.TextField(blank=True, null=True)  # 内容
    image = models.CharField(max_length=50, blank=True, null=True)  # 图片
    sale = models.IntegerField(blank=True, null=True)  # 销量
    comment_count = models.IntegerField(blank=True, null=True)  # 评论次数
    version = models.IntegerField(blank=True, null=True)  # 版本
    page_number = models.IntegerField(blank=True, null=True)  # 页数
    word_number = models.IntegerField(blank=True, null=True)  # 字数
    print_time = models.DateField(blank=True, null=True)  # 印刷时间
    book_size = models.IntegerField(blank=True, null=True)  # 开本
    page_quality = models.CharField(max_length=20, blank=True, null=True)  # 纸张
    book_number = models.CharField(max_length=20, blank=True, null=True)  # 国际编号
    editor_recommend = models.TextField(blank=True, null=True)  # 编辑推荐
    content_recommend = models.TextField(blank=True, null=True)  # 内容推荐
    author_brief = models.TextField(blank=True, null=True)  # 作者简介
    list = models.TextField(blank=True, null=True)  # 目录
    media_comment = models.TextField(blank=True, null=True)  # 媒体推荐
    online_read = models.TextField(blank=True, null=True)  # 在线试读
    print_count = models.IntegerField(blank=True, null=True)  # 印刷次数
    package = models.CharField(max_length=10, blank=True, null=True)  # 包装
    is_suit = models.CharField(max_length=10, blank=True, null=True)  # 是否套装
    category = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)  # 分类id

    # 定义实例方法，用于表示折扣
    def save_price(self):

        return '%.2f' % (self.discount*10/self.price)

    class Meta:
        managed = False
        db_table = 't_book'


class TCategory(models.Model):
    category_name = models.CharField(max_length=20, blank=True, null=True)  # 分类名
    parent_id = models.IntegerField(blank=True, null=True)  # 父类id
    level = models.IntegerField(blank=True, null=True)  # 等级

    class Meta:
        managed = False
        db_table = 't_category'

