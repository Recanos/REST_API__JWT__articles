from .models import Articles
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    # "username" с валидацией на уникальность и ограничением длины
    username = serializers.CharField(
        required=True,
        min_length=3,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Имя пользователя уже используется")]
    )
    # "password" использует встроенные валидаторы пароля Django (PBKDF2 с хешем SHA256)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Имя пользователя должно состоять только из букв и цифр")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'password')

class ArticlesSerializer(serializers.ModelSerializer):
    header = serializers.CharField(max_length=50, min_length=4)
    body = serializers.CharField(min_length=5, max_length=250)
    user = serializers.ReadOnlyField(source='user.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # Получаем пользователя из контекста запроса, установленного viewset
        request = self.context.get('request')
        # Проверяем, авторизован ли пользователь и является ли владельцем статьи
        if request and hasattr(request, 'user'):
            return obj.user == request.user
        return False

    def validate_header(self, value):
        if not value.isprintable():
            raise serializers.ValidationError("Заголовок содержит недопустимые символы")
        return value

    def validate_body(self, value):
        if not value.isprintable():
            raise serializers.ValidationError("Тело статьи содержит недопустимые символы")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('user', None)  # Удалить "user", если он был в запросе, тк ReadOnly
        return super().update(instance, validated_data)

    class Meta:
        model = Articles
        fields = ('user', 'id', 'header', 'body', 'is_owner')
