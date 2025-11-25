from django.conf import settings

def contact_info(request):
    """Make contact information available in all templates"""
    return {
        'CONTACT_MOBILE': getattr(settings, 'CONTACT_MOBILE', ''),
        'CONTACT_PHONE': getattr(settings, 'CONTACT_PHONE', ''),
        'CONTACT_EMAIL': getattr(settings, 'CONTACT_EMAIL', ''),
    }
