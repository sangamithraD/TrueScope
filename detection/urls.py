from django.urls import path
from . import views  # ✅ import all views
from .views import health_check

urlpatterns = [
    path('check-news/', views.check_news, name='check_news'),
    path('map-data/', views.map_data, name='map_data'),
    path('state-news/<str:state_name>/', views.state_news, name='state_news'),
    path('health/', health_check, name='health_check'),
]
