from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import BookSerializer,MemberSerializer,AuthorSerilizer,BorrowRequestSerializer,BorrowHistorySerializers
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .models import Member,Author, Book,BorrowRequest,BorrowHistory
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
import json 
import csv
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from rest_framework.renderers import JSONRenderer

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
           
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            
            if not email or not password:
                return JsonResponse({"error": "Email and password are required!"}, status=400)

           
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User already exists!"}, status=400)

            
            user = User.objects.create_user(username=email, email=email, password=password)
            tokens = generate_tokens(user)

           
            return JsonResponse({
                "message": "User created successfully!",
                "user_id": user.id
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload!"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    elif request.method == 'GET':
    	return JsonResponse({"message": "Create User endpoint is live!"}, status=200)
    return JsonResponse({"error": "Method not allowed!"}, status=405)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def borrow_request(request):
	requests=BorrowRequest.objects.all().values()
	return JsonResponse({"borrow_request":list(requests)})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def approval(request, request_id):
    try:
        borrow_request = BorrowRequest.objects.get(id=request_id)
    except BorrowRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)

    data = request.data
    status = data.get('status')

    if status not in ['approve', 'deny']:
        return JsonResponse({"error": "Invalid status"}, status=400)

    borrow_request.status = status
    borrow_request.save()
    return JsonResponse({"message": f"Request {status} successfully"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_history(request, user_id):
    if not request.user.is_staff and request.user.id != user_id:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    history = BorrowHistory.objects.filter(user_id=user_id).values()
    return JsonResponse({"History": list(history)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_books(request):
    books = Book.objects.all().values()
    return JsonResponse({"Books": list(books)})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_book(request):
    if request.method == "POST":
        try:
           
            data = json.loads(request.body)
            book_id = data.get('book_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

           
            if not book_id or not start_date or not end_date:
                return JsonResponse({'error': 'Missing required fields: book_id, start_date, or end_date'}, status=400)

            
            if not Book.objects.filter(id=book_id).exists():
                return JsonResponse({'error': 'Book not found'}, status=404)

           
            BorrowRequest.objects.create(
                user=request.user,
                book_id=book_id,
                start_date=start_date,
                end_date=end_date
            )

            
            return JsonResponse({"message": "Borrow request submitted successfully"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def peronal_history(request):
	history=BorrowHistory.objects.filter(user=request.user)
	return JsonResponse({'message':list(history)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_borrow_history(request):
    history = BorrowHistory.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="borrow_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Book Title', 'Borrow Date', 'Return Date'])

    for record in history:
        writer.writerow([record.book_instance.book.title, record.borrow_date, record.return_date])

    return response

class JSONOnlyTokenObtainPairView(TokenObtainPairView):
    renderer_classes = [JSONRenderer]

class JSONOnlyTokenRefreshView(TokenRefreshView):
    renderer_classes = [JSONRenderer]

class JSONOnlyTokenVerifyView(TokenVerifyView):
    renderer_classes = [JSONRenderer]