import csv
import io
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



def home(request):
    return render(request, 'index.html')


class AddUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            decode_file = file.read().decode()
            io_string = io.StringIO(decode_file)
            reader = csv.reader(io_string)
            for i in reader:
                password = User.objects.make_random_password()
                User.objects.create(username = i[0] ,first_name = i[0], last_name = i[1], email = i[2], password = password)
            return Response({'msg':'users are created!'})


class UserSetPassword(APIView):
    def get(self, request):
        return Response({'msg':'change password'})
        
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = User.objects.get(username = username)
        user.set_password(password)
        user.save()
        return Response({'msg':'Your password has change'})


class UserChangePassword(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data = request.data, context = {'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password changed successfully'})


