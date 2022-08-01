from rest_framework import viewsets, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from account.models import Profession, Account
from account.serializers import ProfessionSerializer, AccountSerializer, LoginSerializer


class AccountRegisterAPIViews(views.APIView):
    @swagger_auto_schema(request_body=AccountSerializer)
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': str(token.key)})


class LoginView(views.APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        login = request.data.get('email')
        if not Account.objects.filter(email=login).exists():
            return Response(
                f'{login} - does not exists'
            )
        user = Account.objects.get(email=login)
        password = request.data.get('password')
        pass_check = user.check_password(password)
        if not pass_check:
            return Response('email or password incorrect')
        token = Token.objects.get(user=user)
        return Response({'token': str(token.key)})


class ProfessionView(viewsets.ModelViewSet):
    """Information about category """
    queryset = Profession.objects.all().order_by('-id')
    serializer_class = ProfessionSerializer
