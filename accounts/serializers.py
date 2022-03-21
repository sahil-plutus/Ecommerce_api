from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User



class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 122, style = {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 122, style = {'input_type':'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
        else:
            user.set_password(password)
            user.save()
            return attrs



class UserSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class ChangePass(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('username', 'password', )