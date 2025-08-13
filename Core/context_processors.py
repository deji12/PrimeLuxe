from django.contrib.sites.shortcuts import get_current_site
from .models import SiteInformation
from .models import FlashMessage

def site_information(request):
    current_site = get_current_site(request)
    flash_messages = FlashMessage.objects.filter(published=True).order_by('-created_at')
    
    # Use get_or_create to retrieve or create the SiteInformation object
    site_information, created = SiteInformation.objects.get_or_create(site=current_site, defaults={
        'site_name': 'Default Site Name',  # You can provide default values for other fields here
        'logo': '',
        'favicon': '',
        'tiktok_link': '#',
        'facebook_link': '#',
        'twitter_link': '#',
        'instagram_link': '#',
        'contact_email': '',
        'contact_number': '',
        'address': '',
    })

    return {'site_information': site_information, 'flash_messages': flash_messages, 'domain': request.get_host()}
