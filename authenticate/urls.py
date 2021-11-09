from django.conf.urls import url
from authenticate.views import UserRegisterView, UserLoginView

urlpatterns = [
    url(r'^signup', UserRegisterView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    ]