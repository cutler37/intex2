from django.db import models
class Category(models.Model):
    title = models.TextField()

class CurrencyCode(models.Model):
    code = models.TextField()
    
# Create your models here.
class Campaign(models.Model):
    url = models.TextField(default='')
    campaign_id = models.IntegerField(default=-1)
    auto_fb_post_mode = models.BooleanField(default=False)
    category = models.ForeignKey(Category, default = None,on_delete=models.PROTECT)
    currencycode = models.ForeignKey(CurrencyCode,default=None,on_delete=models.PROTECT)
    current_amount = models.DecimalField(max_digits=10, decimal_places =2,default=0)
    goal = models.DecimalField(max_digits=10, decimal_places=2,default =0)
    donators = models.IntegerField(default=0)
    days_active = models.IntegerField(default=0)
    title = models.TextField(default='')
    description = models.TextField(default='')
    default_url = models.TextField(default='')
    has_beneficiary = models.BooleanField(default=False)
    turn_off_donations = models.BooleanField(default=False)
    visible_in_search = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    deactivated = models.BooleanField(default=False)
    state = models.BooleanField(default=False)
    campaign_image_url = models.URLField(default='')
    launch_date = models.DateField(default='')
    campaign_hearts = models.IntegerField(default=0)
    social_share_total =  models.IntegerField(default=0)
    social_share_last_update = models.DateField(default='')
    location_city = models.TextField(default='')
    location_country = models.TextField(default='')
    location_zip = models.IntegerField(default=0)
    is_charity = models.BooleanField(default=False)
    charity_name = models.TextField(default='')
