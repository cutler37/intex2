from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from api import views
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
urlpatterns = [ 
    path('category/', views.CategoryList.as_view()),
    path('user/',views.GetUser.as_view()),
    #search user by name
    path('user/<str:name>',views.GetUserName.as_view()),
    path('login/', views.Login.as_view()),
    #search campaigns, variable is begining place for start of next pages
    path('campaign/<int:numPage>', views.CampaignList.as_view()),
    #search for campaigns based on campaignID
    path('searchcampaigns/<int:campaignID>', views.SearchCampaign.as_view()),
    # search campaigns based on word in descriptions second variable is where to start
    path('SearchCampaignDesc/<str:desc>/<int:numPage>',views.SearchCampaignDesc.as_view()),
    #search campaign title, and second variable is page begining again.
    path('searchwordcampaigns/<str:titles>/<int:numPage>', views.SearchCampaignTitle.as_view()),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]