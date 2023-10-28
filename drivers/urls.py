from django.urls import path

from drivers.views import DriverCreateView, DriverListView, DriverProfileView

urlpatterns = [
    path('create/', DriverCreateView.as_view(), name='create'),
    path('list/', DriverListView.as_view(), name='list'),
    path('profile/', DriverProfileView.as_view(), name='profile'),
]