from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Articles
from rest_framework.test import APITestCase

class ArticlesAPITestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя и сохраняем его в базе данных
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_create_article(self):
        # Тест на создание новой статьи
        self.client.force_authenticate(self.user)  # Проходим аутентификацию
        data = {'header': 'New Article', 'body': 'A great story!'}
        response = self.client.post(reverse('articles-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_article_list(self):
        # Тест на получение списка статей без аутентификации
        response = self.client.get(reverse('articles-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration(self):
        # Тест на регистрацию пользователя
        data = {'username': 'newuser', 'password': 'newpassword123'}
        response = self.client.post(reverse('user_register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_jwt_obtain_pair(self):
        # Тест на получение JWT токенов для аутентифицированного пользователя
        response = self.client.post(reverse('token_obtain_pair'), 
                                    {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

