"""Migrate existing images from Railway to Cloudinary."""
import os
import django
import requests
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.menu.models import Menu
from apps.organizations.models import Organization
from django.core.files.base import ContentFile
import cloudinary
import cloudinary.uploader

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
)

def migrate_menu_images():
    """Migrate menu images to Cloudinary."""
    print("🔄 Starting image migration to Cloudinary...\n")
    
    # Get all menu items with images
    menu_items = Menu.objects.exclude(image_url='').exclude(image_url__isnull=True)
    
    if not menu_items.exists():
        print("❌ No menu items with images found!")
        return
    
    print(f"📋 Found {menu_items.count()} menu items with images\n")
    
    migrated = 0
    failed = 0
    
    for item in menu_items:
        try:
            # Get current image URL
            current_url = item.image_url.url if hasattr(item.image_url, 'url') else str(item.image_url)
            
            print(f"📸 Processing: {item.name}")
            print(f"   Current URL: {current_url}")
            
            # Check if already on Cloudinary
            if 'cloudinary.com' in current_url:
                print(f"   ✅ Already on Cloudinary, skipping\n")
                continue
            
            # Download image from Railway
            if current_url.startswith('http'):
                response = requests.get(current_url, timeout=10)
                if response.status_code == 200:
                    image_content = BytesIO(response.content)
                else:
                    print(f"   ❌ Failed to download: {response.status_code}\n")
                    failed += 1
                    continue
            else:
                # Local file
                try:
                    with open(item.image_url.path, 'rb') as f:
                        image_content = BytesIO(f.read())
                except Exception as e:
                    print(f"   ❌ Failed to read local file: {e}\n")
                    failed += 1
                    continue
            
            # Upload to Cloudinary
            file_name = os.path.basename(current_url)
            result = cloudinary.uploader.upload(
                image_content,
                folder='menu/items',
                public_id=os.path.splitext(file_name)[0],
                overwrite=True,
                resource_type='image'
            )
            
            # Update database with new Cloudinary URL
            new_url = result['secure_url']
            item.image_url = new_url
            item.save(update_fields=['image_url'])
            
            print(f"   ✅ Migrated to: {new_url}\n")
            migrated += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            failed += 1
    
    print("\n" + "="*60)
    print(f"✅ Migration complete!")
    print(f"   Migrated: {migrated}")
    print(f"   Failed: {failed}")
    print(f"   Total: {menu_items.count()}")
    print("="*60)

def migrate_organization_logos():
    """Migrate organization logos to Cloudinary."""
    print("\n🔄 Migrating organization logos...\n")
    
    orgs = Organization.objects.exclude(logo='').exclude(logo__isnull=True)
    
    if not orgs.exists():
        print("❌ No organizations with logos found!")
        return
    
    print(f"📋 Found {orgs.count()} organizations with logos\n")
    
    migrated = 0
    failed = 0
    
    for org in orgs:
        try:
            current_url = org.logo.url if hasattr(org.logo, 'url') else str(org.logo)
            
            print(f"🏢 Processing: {org.name}")
            print(f"   Current URL: {current_url}")
            
            if 'cloudinary.com' in current_url:
                print(f"   ✅ Already on Cloudinary, skipping\n")
                continue
            
            # Download image
            if current_url.startswith('http'):
                response = requests.get(current_url, timeout=10)
                if response.status_code == 200:
                    image_content = BytesIO(response.content)
                else:
                    print(f"   ❌ Failed to download: {response.status_code}\n")
                    failed += 1
                    continue
            else:
                try:
                    with open(org.logo.path, 'rb') as f:
                        image_content = BytesIO(f.read())
                except Exception as e:
                    print(f"   ❌ Failed to read local file: {e}\n")
                    failed += 1
                    continue
            
            # Upload to Cloudinary
            file_name = os.path.basename(current_url)
            result = cloudinary.uploader.upload(
                image_content,
                folder='organizations/logos',
                public_id=os.path.splitext(file_name)[0],
                overwrite=True,
                resource_type='image'
            )
            
            # Update database
            new_url = result['secure_url']
            org.logo = new_url
            org.save(update_fields=['logo'])
            
            print(f"   ✅ Migrated to: {new_url}\n")
            migrated += 1
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            failed += 1
    
    print("\n" + "="*60)
    print(f"✅ Logo migration complete!")
    print(f"   Migrated: {migrated}")
    print(f"   Failed: {failed}")
    print(f"   Total: {orgs.count()}")
    print("="*60)

if __name__ == '__main__':
    # Check Cloudinary configuration
    if not all([
        os.getenv('CLOUDINARY_CLOUD_NAME'),
        os.getenv('CLOUDINARY_API_KEY'),
        os.getenv('CLOUDINARY_API_SECRET')
    ]):
        print("❌ Cloudinary credentials not found in .env file!")
        print("\nPlease add to .env:")
        print("USE_CLOUDINARY=True")
        print("CLOUDINARY_CLOUD_NAME=your-cloud-name")
        print("CLOUDINARY_API_KEY=your-api-key")
        print("CLOUDINARY_API_SECRET=your-api-secret")
        exit(1)
    
    print("☁️  Cloudinary Migration Tool")
    print("="*60)
    print(f"Cloud Name: {os.getenv('CLOUDINARY_CLOUD_NAME')}")
    print("="*60 + "\n")
    
    # Migrate menu images
    migrate_menu_images()
    
    # Migrate organization logos
    migrate_organization_logos()
    
    print("\n🎉 All done! Images are now on Cloudinary.")
    print("💡 Don't forget to add Cloudinary credentials to Railway Variables!")
