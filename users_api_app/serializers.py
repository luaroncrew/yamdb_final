from django.contrib.auth import authenticate

from rest_framework import serializers

from users_api_app.models import CustomUser


class EmailRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такой email уже зарегистрирован'
            )
        return email


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=128, write_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        email = data['email']
        confirmation_code = data['confirmation_code']
        user = authenticate(email=email, password=confirmation_code)

        if user is None:
            raise serializers.ValidationError('Неверные учетные данные')

        data = {
            'email': user.email,
            'user_id': user.pk,
        }

        return data


class UserListSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        initial=CustomUser.USER,
        default=CustomUser.USER,
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
