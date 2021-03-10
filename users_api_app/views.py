from django.contrib.auth.models import update_last_login

from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .permissions import IsAdmin
from .serializers import (EmailRegistrationSerializer, TokenObtainSerializer,
                          UserListSerializer)


class EmailRegistrationView(APIView):
    """
    Получить код доступа (он же пароль), передав свой email.
    Доступ - any.
    """
    serializer_class = EmailRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser(email=email,)
        user.username = email
        password = CustomUser.objects.make_random_password()
        user.set_password(password)
        serializer.save(username=user.username, password=user.password)
        status_code = status.HTTP_201_CREATED

        response = {
            'statusCode': status_code,
            'message': 'Код доступа выслан на вашу электронную почту',
        }

        user.email_user(
            'Код подтверждения',
            f'Ваш код подтверждения - {password}',
            fail_silently=False
        )

        return Response(response, status=status_code)


class TokenObtainCustomView(APIView):
    """
    Получить JWT токен. Доступ к эндпоинту - any.
    """
    serializer_class = TokenObtainSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_201_CREATED

        user = generics.get_object_or_404(
            CustomUser,
            pk=serializer.data['user_id']
        )

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        update_last_login(None, user)

        response = {
            'statusCode': status_code,
            'message': 'Токен получен',
            'access': access_token,
            'refresh': refresh_token,
            'authenticatedUser': {
                'email': user.email,
            }
        }

        return Response(response, status=status_code)


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAdmin,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ['username', ]
    search_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'put', 'patch'],
            permission_classes=(IsAuthenticated,), url_path='me')
    def get_update_user_own_info(self, request):
        """
        Получить и обновить информацию о себе.
        Права доступа - любой авторизованный пользователь.
        """
        current_user = generics.get_object_or_404(
            CustomUser,
            pk=self.request.user.pk
        )
        serializer = UserListSerializer(
            instance=current_user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
