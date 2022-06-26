from datetime import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import F, Q
from product.models import Product as ProductModel

from product.serializers import ProductSerializer
from django_rest_framework.permissions import RegisteredMoreThanThreeDaysUser


# Create your views here.
class ProductView(APIView): # CBV 방식
    
    permission_classes = [RegisteredMoreThanThreeDaysUser]

    # 제품 정보 조회
    def get(self, request):
        today = datetime.now()
        products = ProductModel.objects.filter(
            Q(exposure_end_date__gte=today, is_active=True)|
            Q(user=request.user)
        )
        serialized_data = ProductSerializer(products, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)
        
    
    # 제품 등록
    def post(self, request):
        request.data['user'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)

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