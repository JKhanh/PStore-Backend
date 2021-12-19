from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from userprofile.models import UserProfile

# Create your views here.
class UserProfileViews(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JSONWebTokenAuthentication

    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'True',
                'status_code': status_code,
                'message': 'User Profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'birth_date': user_profile.birth_date,
                    'gender': user_profile.gender,
                    'address': user_profile.address
                    }]
                }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return JsonResponse(response, status=status_code)