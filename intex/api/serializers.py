from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Campaign,Category,CurrencyCode

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['pk','url','campaign_id','auto_fb_post_mode','category','currencycode','current_amount','goal','donators','days_active','title','description','default_url','has_beneficiary','turn_off_donations','visible_in_search','status','deactivated','state','campaign_image_url','launch_date','campaign_hearts','social_share_total','social_share_last_update','location_city','location_country','location_zip','is_charity','charity_name']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'title']
class CurrencyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyCode
        fields = ['pk', 'code']