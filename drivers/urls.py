from django.urls import path

from drivers.views import DriverCreateView, DriverListView

urlpatterns = [
    path('create/', DriverCreateView.as_view(), name='create'),
    path('list/', DriverListView.as_view(), name='list'),
]