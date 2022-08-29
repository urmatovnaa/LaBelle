from django.urls import path
from account.views import AccountRegisterAPIViews, LoginView, ProfessionView


urlpatterns = [
    path('registration/', AccountRegisterAPIViews.as_view(), name='user-registration'),
    path('login/', LoginView.as_view())
    path
]
