from django.urls import path
from . import views
urlpatterns=[
    path('', views.CreateOrderView.as_view()),
    path('own/', views.UserOrderList.as_view()),
    path('own/<int:pk>/', views.UpdateOrderStatusView.as_view()),

]