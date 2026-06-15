import django
from django.conf import settings


def pytest_configure():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "easy_thumbnails",
            "rest_framework",
            "tests",
        ],
        MEDIA_ROOT="/tmp/etr-test-media",
        MEDIA_URL="/media/",
        THUMBNAIL_ALIASES={
            "": {
                "avatar": {"size": (50, 50), "crop": True},
            },
            "tests.Photo.image": {
                "small": {"size": (40, 40), "crop": True},
                "large": {"size": (200, 200), "crop": True},
            },
        },
        USE_TZ=True,
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    )
    django.setup()
