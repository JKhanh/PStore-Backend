from django.conf.urls import url
from userprofile.views import UserProfileViews


urlpatterns = [
    url(r'^profile', UserProfileViews.as_view()),
    ]