from rest_framework import serializers

from account.models import Profession, Account


class AccountSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'fullname', 'username', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        attrs = super().validate(attrs)
        password = attrs['password']
        confirm_password = attrs['confirm_password']
        if password != confirm_password:
            raise serializers.ValidationError(detail='password does not match', code='password_match')
        return attrs

    def create(self, validated_data):
        user = Account.objects.create_user(
            email=validated_data["email"],
            fullname=validated_data["fullname"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'
