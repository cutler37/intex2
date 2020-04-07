from django.shortcuts import render
from api.serializers import CampaignSerializer
from api.models import Campaign,CurrencyCode,Category
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Campaign):
            return str(obj)
        return super().default(obj)
# Create your views here.
class CampaignList (APIView):
    @csrf_exempt
    def get(self, request, format = None):
        otherway = serialize("json", Campaign.objects.all(),cls=LazyEncoder)
        return Response(json.loads(otherway))
    @csrf_exempt
    def post(self,request,format=None):
        prod=request.data
        print("********************************************************************************************")
        print(prod['url'])
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
    def get(self,request,titles,format=None):
        print(titles)
        campaigns = Campaign.objects.filter(title= titles)
        otherway = serialize("json", campaigns,cls=LazyEncoder)
        return Response(json.loads(otherway))

class CategoryList (APIView):
    @csrf_exempt
    def get(self,request,format=None):
        campaigns = Category.objects.all()
        otherway = serialize("json", campaigns,cls=LazyEncoder)
        return Response(json.loads(otherway))