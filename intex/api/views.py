from django.shortcuts import render
from api.serializers import CampaignSerializer
from api.models import Campaign,CurrencyCode,Category

from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class CampaignList (APIView):
    @csrf_exempt
    def get(self, request, format = None):
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns)
        print(serializer)
        return Response(serializer.data)

class SearchCampaign (APIView):
    @csrf_exempt
    def get(self,request,campaignID,format=None):
        print(campaignID)
        campaigns = Campaign.objects.get(campaign_id= campaignID)
        serializer = CampaignSerializer(campaigns)
        return Response(serializer.data)

class SearchCampaignTitle (APIView):
    @csrf_exempt
    def get(self,request,titles,format=None):
        print(titles)
        campaigns = Campaign.objects.filter(title= titles)
        serializer = CampaignSerializer(campaigns)
        return Response(serializer.data)