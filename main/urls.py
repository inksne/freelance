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
    path('authenticated/profile/', MyProfileView, name='my_profile'),
    path('authenticated/profile/<int:user_id>/', UserProfileView, name='user_profile'),
    path('authenticated/order/<int:order_id>/respond/', AddResponse, name='add_response'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/v1/token/refresh-cookie/', RefreshAccessTokenAPIView.as_view(), name='token_refresh'),
    path('api/v1/delete_order/<int:order_id>/', DeleteOrderView, name='delete_order'),
    path('api/v1/delete_review/<int:review_id>/', DeleteReviewView, name='delete_review'),
]