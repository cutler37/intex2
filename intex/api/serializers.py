from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Campaign,Category,CurrencyCode

class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id','url','campaign_id','auto_fb_post_mode','category','currencycode','current_amount','goal','donators','days_active','title','description','default_url','has_beneficiary','turn_off_donations','visible_in_search','status','deactivated','state','campaign_image_url','launch_date','campaign_hearts','social_share_total','social_share_last_update','location_city','location_country','location_zip','is_charity','charity_name']
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
class CurrencyCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyCode
        fields = ['id', 'code']