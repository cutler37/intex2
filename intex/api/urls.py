from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api import views
from django.urls import path
urlpatterns = [ 
    path('category/', views.CategoryList.as_view()),
    path('campaign/', views.CampaignList.as_view()),
    path('searchcampaigns/<int:campaignID>', views.SearchCampaign.as_view()),
    path('searchwordcampaigns/<str:titles>', views.SearchCampaignTitle.as_view()),
]