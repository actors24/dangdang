from home.models import TBook


class Cart:

    def __init__(self):
        self.book_items = []   # 用来存储书的容器

    def add_book(self, id, num):
        book = self.check_book(id)
        if book:
            book.book_num += num
        else:
            book = Book(id, num)
            self.book_items.append(book)

    def del_book(self, id ,num):
        book = self.check_book(id)
        if book:
            self.book_items.remove(book)

    def check_book(self,id):
        for book in self.book_items:
            if id == book.id:
                return book
        return None


class Book:

    def __init__(self, id, num):
        self.id = id
        self.book_name = TBook.objects.get(pk=id).book_name
        self.book_picture = TBook.objects.get(pk=id).image
        self.book_price = TBook.objects.get(pk=id).discount
        self.book_num = num
