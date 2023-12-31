from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.social_login.views import FacebookSocialAuthView, GoogleSocialAuthView
from users.views import (
    PhoneVerifyView,
    SendVerificationCodeView,
    TokenObtainView,
    UserProfileView,
    UserRegisterView, LoginView,
)
from users.views.announcement import AnnouncementCreateView, AnnouncementListView, AnnouncementProfileView

urlpatterns = [
    path("auth/register/", UserRegisterView.as_view(), name="register"),
    path("auth/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("send/verification-code/", SendVerificationCodeView.as_view(), name="send_code"),
    path("verify/phone-number/", PhoneVerifyView.as_view(), name="verify_phone"),
    path("announcement/", AnnouncementCreateView.as_view(), name="Announcement-create"),
    path("announcement/list/", AnnouncementListView.as_view(), name="Announcement-list"),
    path("announcement/<int:pk>/", AnnouncementProfileView.as_view(), name="Announcement-detail"),
    # path("auth/faceobok/", FacebookSocialAuthView.as_view(), name="facebook_login"),
    # path("auth/google/", GoogleSocialAuthView.as_view(), name="google_login"),
]
