from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import User, JobSeekerProfile, RecruiterProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    JobSeekerProfileSerializer,
    RecruiterProfileSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)
from django.contrib.auth.hashers import check_password

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to register
    
    def post(self, request):
        print(f"Registration attempt with data: {request.data}")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer is valid, creating user...")
            user = serializer.save()
            print(f"User created with ID: {user.id}, username: {user.username}")
            print(f"Password hash: {user.password[:20]}...")
            
            # Create appropriate profile based on role
            if user.role == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)
                print(f"Created job seeker profile for {user.username}")
            elif user.role == 'recruiter':
                RecruiterProfile.objects.create(user=user)
                print(f"Created recruiter profile for {user.username}")
            
            test_auth = authenticate(request, username=request.data['username'], password=request.data['password'])
            if test_auth:
                print(f"Test authentication successful for {user.username}")
            else:
                print(f"Warning: Test authentication failed for {user.username}")
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({
                'message': 'User registered successfully',
                'user': UserProfileSerializer(user).data,
                'access': access_token,
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
            
        print(f"Registration failed. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to login
    
    def post(self, request):
        print(f"Login attempt with data: {request.data}")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(username=username)
                print(f"Found user: {user.username}, ID: {user.id}")
                
                # Try authentication without request context first
                auth_user = authenticate(username=username, password=password)
                if not auth_user:
                    # Try with request context if first attempt fails
                    auth_user = authenticate(request, username=username, password=password)
                
                print(f"Authentication result: {'Success' if auth_user else 'Failed'}")
                
                if auth_user:
                    refresh = RefreshToken.for_user(auth_user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': UserProfileSerializer(auth_user).data
                    })
                else:
                    # Check password manually
                    is_password_valid = check_password(password, user.password)
                    print(f"Manual password check: {'Valid' if is_password_valid else 'Invalid'}")
                    
                    if is_password_valid:
                        # If password is valid but authentication failed, create tokens manually
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': UserProfileSerializer(user).data
                        })
                    
                    return Response({
                        'error': 'Invalid credentials',
                        'detail': 'Password verification failed'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except User.DoesNotExist:
                print(f"No user found with username: {username}")
                return Response({
                    'error': 'Invalid credentials',
                    'detail': 'User not found'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.job_seeker_profile
        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.job_seeker_profile
        serializer = JobSeekerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruiterProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.recruiter_profile
        serializer = RecruiterProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.recruiter_profile
        serializer = RecruiterProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = RefreshToken.for_user(user).access_token
                reset_link = f"{settings.FRONTEND_URL}/reset-password/{token}"
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset link sent to your email'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            # Implement token verification and password reset logic here
            return Response({'message': 'Password reset successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 