from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("basket/", ApplyBasket.as_view()),
    path("basket/<int:basket_id>/", BasketDetail.as_view()),
    path("baskets/", BasketList.as_view()),
]
