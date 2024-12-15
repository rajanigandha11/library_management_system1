from rest_framework import serializers
from .models import Member,Book,Author,BorrowRequest,BorrowHistory


class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model=Book
		fields=['id','title','author','price','publication','date_of_publish','quantity','genere']

class MemberSerializer(serializers.ModelSerializer):
	class Meta:
		model=Member
		fields=['id','user','phone','address','join_date']

class AuthorSerilizer(serializers.ModelSerializer):
	class Meta:
		model=Author
		fields=['id','first_name','last_name','date_of_birth']

class BorrowRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=BorrowRequest
		fields=['id','user','book','start_date','end_date','status']

class BorrowHistorySerializers(serializers.ModelSerializer):
	class Meta:
		model=BorrowHistory
		fields=['id','member','book_instance','issue_date','return_date','trans_status']