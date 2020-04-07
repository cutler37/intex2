#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'intex.settings'
import django
django.setup()

# regular imports
from api.models import Category, Campaign, CurrencyCode
import json

# main script
def main():
    
    print('start script')
    # read the json data
    with open('data.json', encoding = "utf8") as json_data:
        data = json.load(json_data)
        print("opens")
    cats = {}
    concur = {}
    y = 1
    i = 1

    # find the categories, and replace them with the
    # new category id (created below)
    for prod in data:
        if prod['category'] not in cats:
            cats[prod['category']] = i
            i += 1
        if prod['currencycode'] not in concur:
            concur[prod['currencycode']] = y
            y += 1
        prod['category'] = cats[prod['category']]
        prod['currencycode'] = concur[prod['currencycode']]
    # create the categories

    for cat_name, cat_id in cats.items():
        new_cat = Category()
        new_cat.id = cat_id
        new_cat.title = cat_name
        new_cat.save()
        
    for concur_code, curr_id in concur.items():
        new_code = CurrencyCode()
        new_code.id = curr_id
        new_code.code = concur_code
        new_code.save()
    # create the products
    for prod in data:
        p = Campaign()
        p.url = prod['url']
        p.campaign_id = prod['campaign_id']
        if prod['auto_fb_post_mode'] ==1:
            p.auto_fb_post_mode= True
        else:
            p.auto_fb_post_mode = False
        p.current_amount = prod['current_amount']
        p.category = Category.objects.get(id=prod['category'])
        p.currencycode = CurrencyCode.objects.get(id=prod['currencycode'])
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
        p.riskScore = prod['riskScore']
        p.save()
        print('saved')

    
    
if __name__ == '__main__':
    main()
