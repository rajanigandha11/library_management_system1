from django.contrib import admin
from .models import Member,Book,Author,BorrowRequest,BorrowHistory

class MemberAdmin(admin.ModelAdmin):
	list_display=['id','user','phone','address','join_date']

admin.site.register(Member,MemberAdmin)

class AuthorAdmin(admin.ModelAdmin):
	list_display=['id','first_name','last_name','date_of_birth']
admin.site.register(Author,AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
	list_display=['id','title','author','price','publication','date_of_publish','quantity','genere']

admin.site.register(Book,BookAdmin)



class BorrowRequestAdmin(admin.ModelAdmin):
	list_display=['id','user','book','start_date','end_date','status']
admin.site.register(BorrowRequest,BorrowRequestAdmin)

class BorrowHistoryAdmin(admin.ModelAdmin):
	list_display=['id','user','book','borrow_date','return_date']

admin.site.register(BorrowHistory,BorrowHistoryAdmin)