from django.conf.urls import include, url
from dsrs import views
from . import views
from django.urls import path
from .views import  RegistrationAPI, LoginAPI, LogoutAPI, ChangePasswordView, DSPViewSet, DSRViewSet


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('register/', RegistrationAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]

urlpatterns += [
    url(r'^', DSRViewSet.as_view({'get': 'list'}), name="dsrs-list"),
    url(r'^resources/percentile/', DSPViewSet.as_view({'get': 'list'}),name="dsp"),
]