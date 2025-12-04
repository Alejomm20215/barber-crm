import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from django.core.management import call_command  # noqa: E402


def setup():
    print("🔄 Running migrations...")
    call_command("migrate")

    print("👤 Checking superuser...")
    if not User.objects.filter(username="admin").exists():
        print("Creating superuser 'admin' with password 'admin'...")
        admin = User.objects.create_superuser("admin", "admin@example.com", "admin")
    else:
        print("Superuser 'admin' already exists.")
        admin = User.objects.get(username="admin")

    # Ensure admin is master
    if hasattr(admin, "profile"):
        admin.profile.is_master = True
        admin.profile.save()
        print("✅ Admin user set as Master Account")

    print("📦 Creating sample data...")
    # Import sample data creation logic
    # We can just exec the existing file to avoid code duplication
    if os.path.exists("create_sample_data.py"):
        with open("create_sample_data.py", "r") as f:
            exec(f.read())
    else:
        print("⚠️ create_sample_data.py not found. Skipping sample data creation.")


if __name__ == "__main__":
    setup()
