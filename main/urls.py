from django.urls import path
from .views import *
from .auth import *

urlpatterns = [
    path('', OrdersView, name='base'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('about_us', AboutUsView, name='about_us'),
    path('register/', RegisterView.as_view(), name='register'),
    path('authenticated/', AuthOrdersView, name='authenticated'),
    path('authenticated/create_order/', AddOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/respond/', AddResponse, name='add_response'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/v1/token/refresh-cookie/', RefreshAccessTokenAPIView.as_view(), name='token_refresh'),
]