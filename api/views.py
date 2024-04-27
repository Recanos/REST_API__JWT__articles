from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Articles
from .permissions import IsAuthenticatedAndOwnerOrReadOnly
from .serializers import ArticlesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from .filters import ArticleFilter

# Регистрация пользователя
@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Создаем токен обновления и доступа для пользователя
        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticlesModelViewSet(ModelViewSet):
    queryset = Articles.objects.all().order_by('-created_at')
    serializer_class = ArticlesSerializer

    # Используем ArticleFilter для определения логики фильтрации
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    permission_classes = [IsAuthenticatedAndOwnerOrReadOnly]