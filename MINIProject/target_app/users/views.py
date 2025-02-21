from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer, UserRegistrationSerializer

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            auth_login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return redirect('base')  # Redirect to home page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
            
    return render(request, 'login.html')

def register(request):
    print("register")
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create token for the new user
        token, _ = Token.objects.get_or_create(user=user)
        
        # Log the user in
        auth_login(request, user)
        return redirect('base')  # Redirect to home page after registration
        
    return render(request, 'register.html')

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def upload_profile_image(self, request, pk=None):
        user = self.get_object()
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.profile_image = request.FILES['image']
        user.save()
        return Response(
            {'message': 'Profile image updated successfully'},
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)