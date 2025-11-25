"""Test OTP functionality"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'josmee_projects.settings')
django.setup()

from accounts.otp_utils import generate_otp, send_otp_via_twilio, create_otp_record

def test_otp():
    print("🧪 Testing OTP Functionality\n")
    
    # Test 1: Generate OTP
    otp = generate_otp()
    print(f"✅ Generated OTP: {otp}")
    print(f"   Length: {len(otp)} digits\n")
    
    # Test 2: Create OTP record
    test_phone = "9876543210"
    otp_obj = create_otp_record(test_phone)
    print(f"✅ Created OTP record for {test_phone}")
    print(f"   OTP: {otp_obj.otp}")
    print(f"   Expires at: {otp_obj.expires_at}\n")
    
    # Test 3: Send OTP
    success, result = send_otp_via_twilio(test_phone, otp_obj.otp)
    print(f"✅ OTP Send Status: {'Success' if success else 'Failed'}")
    print(f"   Result: {result}\n")
    
    print("💡 Note: Check console for OTP if Twilio is not configured")
    print("💡 Note: OTP codes will be printed for testing purposes")

if __name__ == '__main__':
    test_otp()
