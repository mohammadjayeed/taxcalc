import requests
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .serializers import TaxCalculationSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet # ViewSet
from .serializers import ProductSerializer
from .models import Product

@swagger_auto_schema(method='post', request_body=TaxCalculationSerializer)
@api_view(['POST'])
def calculate_tax(request):
    serializer = TaxCalculationSerializer(data=request.data)
    if serializer.is_valid():
        
        street =  serializer.validated_data['street']
        city =  serializer.validated_data['city']
        state =  serializer.validated_data['state']
        zip =  serializer.validated_data['zip']
        amount =  serializer.validated_data['amount']
        shipping = serializer.validated_data.get('shipping',0)
        
        
        bearer_token = '0c3927264e89260b1e79205e3d5ca4c4'
        
        
        other_api_url = 'https://api.taxjar.com/v2/taxes'
        
        data ={
    
            "to_country": "US",
            "to_zip": zip,
            "to_state": state,
            "amount": amount,
            "shipping": shipping
        }
        headers = {'Authorization': f'Bearer {bearer_token}'}
        response = requests.post(other_api_url, data=data, headers=headers)
        
        tax_data = response.json()
        print(tax_data)
        if response.status_code == 200:   
            amount_to_collect = tax_data.get('tax', {}).get('amount_to_collect', 0)
            return Response({'tax': amount_to_collect})
        elif response.status_code in [400,401]:
            return Response({'error': f"{tax_data['error']}", 'detail':f"{tax_data['detail']}"}, status=response.status_code)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        queryset = Product.objects.filter(title=request.data['title']).exists()
        serializer = ProductSerializer(data=request.data)

        print(queryset)
        if queryset:
            return Response({"status": "error","message": 'product already exists'}, status.HTTP_400_BAD_REQUEST)
            


        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        serializer.save()
        return Response({"status": "success","message": "product created."}, status.HTTP_201_CREATED)
            



        

        