import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaxCalculationSerializer
from rest_framework import status

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
        
        
        if response.status_code == 200:
            tax_data = response.json()
            tax = tax_data.get('amount_to_collect', 0)  
            return Response({'tax': tax})
        elif response.status_code in [400,401]:
            # Handle error response from the other API
            return Response({'error': f'{tax_data['error']}'}, status=response.status_code)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
