from django.shortcuts import render

from api.models import Campaign,CurrencyCode,Category,User
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
import hashlib
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import datetime
from django.contrib.auth import authenticate
import json
import random
from .serializers import CustomUserSerializer

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Campaign):
            return str(obj)
        return super().default(obj)
# Create your views here.
class GetUser (APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def get(self, request, format = None):
        otherway = serialize("json", User.objects.all()[:100],cls=LazyEncoder)
        return Response(json.loads(otherway))

    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request,format = None):
        prod = request.data
        if User.objects.filter(Username = prod['Username']):
            user =  User.objects.get(Username = prod['Username'])
            
            string = prod['Password']+user.salt
            if user.Password == hashlib.sha256(str(string).encode('utf-8')).hexdigest():
                validate = True
                return Response({"validated"})
        
        return Response({"Error validating"})

class GetUserName (APIView):
    @csrf_exempt
    def get(self, request,name, format = None):
        otherway = serialize("json", User.objects.filter(Username = name),cls=LazyEncoder)
        return Response(json.loads(otherway))
        
class CampaignList (APIView):
    @csrf_exempt
    def get(self, request,numPage=0, format = None):
        print(numPage)
        numPerPage  =25 
        otherway = serialize("json", Campaign.objects.all()[numPage:numPage+numPerPage],cls=LazyEncoder)
        return Response(json.loads(otherway))

    @csrf_exempt
    def post(self,request,format=None):
        prod=request.data
        p = Campaign()
        p.url = prod['url']
        p.campaign_id = prod['campaign_id']
        if prod['auto_fb_post_mode'] ==1:
            p.auto_fb_post_mode= True
        else:
            p.auto_fb_post_mode = False
        p.current_amount = prod['current_amount']
        p.category = Category.objects.get(title=prod['category'])
        p.currencycode = CurrencyCode.objects.get(code=prod['currencycode'])
        p.donators = prod['donators']
        
        if  isinstance(prod['days_active'], int):
            p.days_active = prod['days_active']
        else :
            p.days_active =0
        p.title = prod['title']
        p.description = prod['description']
        p.default_url = prod['default_url']
        if prod['has_beneficiary'] ==1:
            p.has_beneficiary= True
        else:
            p.has_beneficiary = False
        if prod['turn_off_donations'] ==1:
            p.turn_off_donations = True
        else:
            p.turn_off_donations = False
        if prod['visible_in_search'] ==1:
            p.visible_in_search = True
        else:
            p.visible_in_search = False
        if prod['status'] ==1:
            p.status = True
        else:
            p.status = False
        if prod['deactivated'] ==1:
            p.deactivated = True
        else:
            p.deactivated = False
        if prod['state'] ==1:
            p.state = True
        else:
            p.state = False
        p.campaign_image_url = prod['campaign_image_url']
        if p.launch_date == '':
            prod['launch_date']= '1970-01-01'
        p.launch_date = prod['launch_date']
        p.campaign_hearts = prod['campaign_hearts']
        p.social_share_total = prod['social_share_total']
        if p.social_share_last_update == '':
            prod['social_share_last_update']= '1970-01-01'
        p.social_share_last_update = prod['social_share_last_update']
        p.location_city = prod['location_city']
        p.location_country = prod['location_country']
        if prod['location_zip'] =='':
            prod['location_zip'] =0
        p.location_zip = prod['location_zip']
        if prod['is_charity'] ==1:
            p.is_charity = True
        else:
            p.is_charity = False
        p.charity_name = prod['charity_name']
        #p.save()
        return Response({"Created"},status=status.HTTP_201_CREATED)
        

class SearchCampaign (APIView):
    @csrf_exempt
    def get(self,request,campaignID,format=None):
        print(campaignID)
        otherway = serialize("json", Campaign.objects.filter(campaign_id= campaignID),cls=LazyEncoder)
        return Response(json.loads(otherway))

class SearchCampaignTitle (APIView):
    @csrf_exempt
    def get(self,request,titles,numPage=0,format=None):
        print(titles)
        campaigns = Campaign.objects.filter(title__contains = titles)[numPage:numPage+25]
        otherway = serialize("json", campaigns,cls=LazyEncoder)
        return Response(json.loads(otherway))

class SearchCampaignDesc (APIView):
    @csrf_exempt
    def get(self,request,desc,numPage=0,format=None):
        print(desc)
        campaigns = Campaign.objects.filter(description__contains = desc)[numPage:numPage+25]
        otherway = serialize("json", campaigns,cls=LazyEncoder)
        return Response(json.loads(otherway))

class CategoryList (APIView):
    @csrf_exempt
    def get(self,request,format=None):
        campaigns = Category.objects.all()
        otherway = serialize("json", campaigns,cls=LazyEncoder)
        return Response(json.loads(otherway))

class CreatePrediction(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        body = json.loads(request.body)
        print(body)
        print("***** we made it here! ******")
        data =  {
                "Inputs": {
                    "input1":
                    {
                        "ColumnNames": ["goal", "days_active", "has_beneficiary", "visible_in_search", "campaign_hearts", "is_charity"],
                        "Values": [[ body['goal'], body['days_active'], body['has_beneficiary'],body['visible_in_search'], body['campaign_hearts'], body['is_charity']],]
                    }, # in the values array above it may seem weird to put a value for the response var, but azure needs something
                },
                "GlobalParameters": {
                }
        }
        # the API call
        api_body = str.encode(json.dumps(data))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/f7ecca118a3b46edab031906e04ea725/services/7cc3b91c7f554575877370c24beee235/execute?api-version=2.0&details=true'
        api_key = 'zY5Oie1v2gd8x7JUU+6t+eD06SSGIu3cSGLqJykxAKnI3fmvx3oTVwT9h8T9dGYZ5mqwfu/LswXXYCt3E1QKUQ=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        print(url, api_body, headers )
        req = urllib.request.Request(url, api_body, headers) 
        response = urllib.request.urlopen(req)
        print(response)
        result = response.read()
        result = json.loads(result) # turns bits into json object
        result = result["Results"]["output1"]["value"]["Values"][0][0] 
        print(result)
        return Response(result)
