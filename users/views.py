import logging
import json
from django.utils import timezone
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserLoginSerializer, TimeSerializer, StatsSerializer
from .utils import generate_otp, log_otp

logger = logging.getLogger(__name__)

# In-memory OTP storage as fallback when Redis is not available
OTP_STORAGE = {}

class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            
            # Create or get user
            user, created = User.objects.get_or_create(mobile=mobile)
            
            # Generate OTP
            otp = generate_otp()
            
            try:
                # Try to store OTP in Redis for 5 minutes
                cache.set(f"otp_{mobile}", otp, timeout=300)
            except Exception as e:
                # Fallback: store OTP in memory if Redis is not available
                logger.warning(f"Redis connection failed: {str(e)}. Using in-memory storage.")
                OTP_STORAGE[f"otp_{mobile}"] = otp
            
            # Log OTP
            log_otp(mobile, otp)
            
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NowAPIView(APIView):
    def get(self, request):
        # Get current time
        current_time = timezone.now()
        
        # Try to get mobile from headers
        mobile = request.META.get('HTTP_AUTHORIZATION', None)
        
        if mobile:
            # Increment request count for this user if they exist
            try:
                user = User.objects.get(mobile=mobile)
                user.now_request_count += 1
                user.save()
            except User.DoesNotExist:
                # Create the user if they don't exist yet
                user = User.objects.create(mobile=mobile, now_request_count=1)
        
        serializer = TimeSerializer({"now": current_time})
        return Response(serializer.data)

class StatsAPIView(APIView):
    def get(self, request):
        # Get mobile from headers
        mobile = request.META.get('HTTP_AUTHORIZATION', None)
        
        if not mobile:
            return Response(
                {"error": "Please provide mobile in Authorization header"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(mobile=mobile)
            data = {
                "user": user.mobile,
                "open_count": user.now_request_count
            }
            serializer = StatsSerializer(data)
            return Response(serializer.data)
        except User.DoesNotExist:
            # Create new user with count 0 if not found
            user = User.objects.create(mobile=mobile, now_request_count=0)
            data = {
                "user": user.mobile,
                "open_count": user.now_request_count
            }
            serializer = StatsSerializer(data)
            return Response(serializer.data)