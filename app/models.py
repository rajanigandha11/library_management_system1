from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	
	phone= models.IntegerField(null=False)
	address=models.CharField(max_length=200)
	join_date=models.DateField(auto_now_add=True)

	def __str__(self):
		return self.user


class Author(models.Model):
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	date_of_birth=models.DateField(auto_now_add=True)
	

	def __str__(self):
		 return f"{self.first_name} {self.last_name}"
	

class Book(models.Model):
	title=models.CharField(max_length=100)
	author=models.ForeignKey(Author,on_delete=models.CASCADE)
	price=models.FloatField()
	publication=models.CharField(max_length=100)
	date_of_publish=models.DateField(auto_now_add=True)
	quantity=models.PositiveIntegerField()
	genere=models.CharField(max_length=200)

	def __str__(self):
		return self.title

class BorrowRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"

class BorrowHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"