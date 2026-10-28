SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if not DEBUG else []
TIME_ZONE = "Asia/Kolkata"
# delete STATICFILES_DIRS until public/static actually exists
# add 'port': 587 inside MAILERS OPTIONS, then run sendtestemail to confirm