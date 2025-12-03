import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.management import call_command

def setup():
    print("🔄 Running migrations...")
    call_command('migrate')
    
    print("👤 Checking superuser...")
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser 'admin' with password 'admin'...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    else:
        print("Superuser 'admin' already exists.")

    print("📦 Creating sample data...")
    # Import sample data creation logic
    # We can just exec the existing file to avoid code duplication
    with open('create_sample_data.py', 'r') as f:
        exec(f.read())

if __name__ == '__main__':
    setup()
