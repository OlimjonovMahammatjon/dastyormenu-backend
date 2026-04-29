"""Test Cloudinary connection and configuration."""
import os
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
import cloudinary
import cloudinary.api

def test_cloudinary():
    """Test Cloudinary configuration."""
    print("☁️  Cloudinary Configuration Test")
    print("="*60)
    
    # Check environment variables
    print("\n1️⃣ Environment Variables:")
    use_cloudinary = os.getenv('USE_CLOUDINARY')
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    
    print(f"   USE_CLOUDINARY: {use_cloudinary}")
    print(f"   CLOUD_NAME: {cloud_name}")
    print(f"   API_KEY: {api_key[:10]}..." if api_key else "   API_KEY: Not set")
    print(f"   API_SECRET: {api_secret[:10]}..." if api_secret else "   API_SECRET: Not set")
    
    if not all([use_cloudinary == 'True', cloud_name, api_key, api_secret]):
        print("\n❌ Cloudinary credentials incomplete!")
        print("\nPlease update .env file with:")
        print("USE_CLOUDINARY=True")
        print("CLOUDINARY_CLOUD_NAME=your-cloud-name")
        print("CLOUDINARY_API_KEY=your-api-key")
        print("CLOUDINARY_API_SECRET=your-api-secret")
        return False
    
    # Check Django settings
    print("\n2️⃣ Django Settings:")
    print(f"   USE_CLOUDINARY: {settings.USE_CLOUDINARY}")
    print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    if hasattr(settings, 'MEDIA_URL'):
        print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    
    if not settings.USE_CLOUDINARY:
        print("\n❌ Cloudinary not enabled in Django settings!")
        return False
    
    # Test Cloudinary connection
    print("\n3️⃣ Testing Cloudinary Connection:")
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
        
        # Ping Cloudinary API
        result = cloudinary.api.ping()
        print(f"   Status: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'ok':
            print("\n✅ Cloudinary connection successful!")
            
            # Get usage info
            try:
                usage = cloudinary.api.usage()
                print("\n4️⃣ Account Usage:")
                print(f"   Plan: {usage.get('plan', 'unknown')}")
                print(f"   Credits: {usage.get('credits', {}).get('usage', 0):,}")
                print(f"   Bandwidth: {usage.get('bandwidth', {}).get('usage', 0):,} bytes")
                print(f"   Storage: {usage.get('storage', {}).get('usage', 0):,} bytes")
                print(f"   Transformations: {usage.get('transformations', {}).get('usage', 0):,}")
            except Exception as e:
                print(f"\n⚠️  Could not fetch usage info: {e}")
            
            return True
        else:
            print(f"\n❌ Cloudinary ping failed: {result}")
            return False
            
    except Exception as e:
        print(f"\n❌ Cloudinary connection failed: {e}")
        print("\nPlease check your credentials:")
        print("1. Go to https://console.cloudinary.com")
        print("2. Copy Cloud Name, API Key, and API Secret")
        print("3. Update .env file")
        return False
    
    print("="*60)

if __name__ == '__main__':
    success = test_cloudinary()
    
    if success:
        print("\n🎉 Everything is configured correctly!")
        print("\n📝 Next steps:")
        print("1. Upload images via Admin Panel or API")
        print("2. Images will automatically be stored on Cloudinary")
        print("3. URLs will be served from Cloudinary CDN")
        print("\n💡 To migrate existing images:")
        print("   python migrate_images_to_cloudinary.py")
    else:
        print("\n❌ Configuration incomplete. Please fix the issues above.")
    
    print("\n" + "="*60)
