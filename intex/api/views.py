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