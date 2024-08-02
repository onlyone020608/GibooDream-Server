from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import *
from donations.models import *
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# Create your views here.

def index(request):
  return HttpResponse("Hi")

class ApplyBasket(APIView):
  def post(self, request, format=None):
    serializer_data = {
      'benefit_name': request.data.get('userName'),
      'buy_num': request.data.get('totalNum'),
      'buy_reason': request.data.get('buy_reason'),
      'basket_apply':124,
      'basket_items': request.data.get('items')
    }
    if(serializer.is_valid()):
      if (request.data.get('basketType')=="dream") :
        serializer = DreamBasketSerializer(data=serializer_data)
        serializer.save()
      else:
        serializer = HeartBasketSerializer(data=serializer_data)
        serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request):
    basketItem = Basket_Item_dream.objects.get(basket_item_id=request.basket_item_id)
    basketItem.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  def put(self, request):
    basketItem = Basket_Item_dream.objects.get(basket_item_id=request.basket_item_id)
    Item = Basket_Item_dream.objects.get(goods_id=request.basket_item_id)
    if(request.data.cal=="add"):
      serializer_data = {
        'basket_dream': basketItem.basket_dream,
        'basket_heart': basketItem.basket_heart,
        'basket_goods_id': basketItem.basket_goods_id,
        'basket_buy_num': basketItem.basket_buy_num + 1,
        'total_price': basketItem.total_price + Item.goods_price
      }
    else:
      serializer_data = {
        'basket_dream': basketItem.basket_dream,
        'basket_heart': basketItem.basket_heart,
        'basket_goods_id': basketItem.basket_goods_id,
        'basket_buy_num': basketItem.basket_buy_num - 1,
        'total_price': basketItem.total_price - Item.goods_price
      }
      
    serializer = BasketItemSerializer(serializer_data)
    serializer.save()
    return Response(serializer.data)

  

class BasketDream(APIView): 
  def get(self, request):
    basket = Basket_dream.objects.get(user_id=request.user_id)
    serializer = DreamBasketSerializer(basket)
    return Response(serializer.data)
  
  def put(self, request):
    basket = Basket_dream.objects.get(basket_id=request.basket_id)
    serializer = DreamBasketSerializer(basket, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request):
    basket = Basket_dream.objects.get(basket_id=request.basket_id)
    basket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)      

class BasketHeart(APIView): 
  def get(self, request):
    basket = Basket_heart.objects.get(user_id=request.user_id)
    serializer = HeartBasketSerializer(basket)
    return Response(serializer.data)
  
  def put(self, request):
    basket = Basket_heart.objects.get(basket_id=request.basket_id)
    serializer = HeartBasketSerializer(basket, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self, request):
    basket = Basket_heart.objects.get(basket_id=request.basket_id)
    basket.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)      


class BasketList(APIView):
  def get(self,request):
    if(request.data.get('basketType')=="dream"):
      baskets = Basket_dream.objects.all()
      serializer = DreamBasketSerializer(baskets, many=True)
    else:
      baskets = Basket_heart.objects.all()
      serializer = HeartBasketSerializer(baskets, many=True)

    return Response(serializer.data)
    


  
  




