# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from api.models import User
# from api.serializers import UserSerializer
# from rest_framework import status
#
# @api_view(['POST', 'GET'])
# def CreateUsers(request, format=None):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response({'users': serializer.data}, status=status.HTTP_200_OK)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def Users(request, user_id, format=None):
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_200_OK)


from rest_framework import generics
from .models import MedicalClearance
from .serializers import MedicalClearanceSerializer
from django.shortcuts import get_object_or_404


class MedicalClearanceDetailView(generics.RetrieveAPIView):
    queryset = MedicalClearance.objects.all()
    serializer_class = MedicalClearanceSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(MedicalClearance, user_id=user_id)
