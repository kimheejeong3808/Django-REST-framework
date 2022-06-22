from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import F, Q
from product.models import Product as ProductModel

from product.serializers import ProductSerializer


# Create your views here.
class ProductView(APIView): # CBV 방식

    # 제품 정보 조회
    def get(self, request):
        today = datetime.now()
        products = ProductModel.objects.filter(
            Q(exposure_start__lte=today, exposure_finish__gte=today,)|
            Q(user=request.user)
        )
        serialized_data = ProductSerializer(products, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
        
        
    
    # 제품 등록
    def post(self, request):
        # user = request.user
        # request.data 안에는 포스트맨에서 작성해준 내용들이 있음
        # user에 대한 정보는 request.user에 있음
        # 그러므로 시리얼라이저에 넣기 위해 user정보를 request.day에 넣어줘야함
        request.data['user'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)
        
        # 반드시 is_valid를 하고 save함
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    def put(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        # product는 기존의 내용/ data는 새로 수정한 내용 / partial 일부 수정 허용
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        else:
            Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    # 등록 삭제
    def delete(self, request):
        return Response({'message': 'delete method!!'})