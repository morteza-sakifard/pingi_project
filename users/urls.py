from django.urls import path
from .views import LoginAPIView, NowAPIView, StatsAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('now/', NowAPIView.as_view(), name='now'),
    path('stats/', StatsAPIView.as_view(), name='stats'),
]