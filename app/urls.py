from django.urls import path
from app import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns=[

	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
	path('create/',views.create_user,name='create'),
	path('borrow_request/',views.borrow_request,name='borrow_request'),
	path('approval/<int:request_id>',views.approval,name='approval'),
	path('user_history/<int:user_id>',views.user_history,name='user_history'),
	path('view_books/',views.view_books,name='view_books'),
	path('request_book/',views.request_book,name='request_book'),
	path('peronal_history/',views.peronal_history,name='peronal_history'),
] 