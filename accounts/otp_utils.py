import random
import string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_via_twilio(phone_number, otp):
    """Send OTP via Twilio SMS"""
    if not settings.TWILIO_FROM_NUMBER:
        print("⚠️ Warning: TWILIO_FROM_NUMBER not configured in settings.py")
        print(f"📱 Simulated OTP for {phone_number}: {otp}")
        return True, "simulated"  # Return success in development mode
    
    try:
        from twilio.rest import Client
        
        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Format phone number (add +91 for India if not present)
        if not phone_number.startswith('+'):
            phone_number = f'+91{phone_number}'
        
        # Send SMS
        message = client.messages.create(
            body=f'Your Josmee verification code is: {otp}. Valid for 10 minutes.',
            from_=settings.TWILIO_FROM_NUMBER,
            to=phone_number
        )
        
        return True, message.sid
    except ImportError:
        print("⚠️ Twilio library not installed. Install with: pip install twilio")
        print(f"📱 Simulated OTP for {phone_number}: {otp}")
        return True, "simulated"
    except Exception as e:
        print(f"❌ Twilio Error: {str(e)}")
        print(f"📱 Simulated OTP for {phone_number}: {otp}")
        # Return success anyway for development
        return True, "simulated"

def verify_otp(phone_number, otp_code):
    """Verify OTP code"""
    from .models import OTPVerification
    
    try:
        otp_obj = OTPVerification.objects.filter(
            phone=phone_number,
            otp=otp_code,
            is_verified=False
        ).latest('created_at')
        
        if otp_obj.is_expired():
            return False, "OTP has expired"
        
        otp_obj.is_verified = True
        otp_obj.save()
        return True, "OTP verified successfully"
    except OTPVerification.DoesNotExist:
        return False, "Invalid OTP"

def create_otp_record(phone_number):
    """Create new OTP record"""
    from .models import OTPVerification
    
    otp_code = generate_otp()
    expires_at = timezone.now() + timedelta(minutes=10)
    
    otp_obj = OTPVerification.objects.create(
        phone=phone_number,
        otp=otp_code,
        expires_at=expires_at
    )
    
    return otp_obj
