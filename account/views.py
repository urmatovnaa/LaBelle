from rest_framework import viewsets, views, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from account.models import Account, Rating
from account.serializers import AccountSerializer, LoginSerializer, MyUserRatingSerializer


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


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    queryset = Rating.objects.all()
    serializer_class = MyUserRatingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            product_id=kwargs.get('product_pk')
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)



