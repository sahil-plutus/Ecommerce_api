from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView, TokenVerifyView
from django.urls import path
from . import views


urlpatterns = [
    # path("register/", views.RegisterView.as_view()),
    path('', views.home, name='home'),
    path('get_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('varify_token/', TokenVerifyView.as_view(), name = 'varify_token'),
    path('adduser/', views.AddUser.as_view(), name = "Add_user"),
    path('setpass/', views.UserSetPassword.as_view(), name = "set_pass"),
    path('changepass/', views.UserChangePassword.as_view(), name = "change_pass"),
]