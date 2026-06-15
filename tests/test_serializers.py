import io

import pytest
from PIL import Image


def _build_request():
    from rest_framework.request import Request
    from rest_framework.test import APIRequestFactory

    return Request(APIRequestFactory().get("/"))


@pytest.fixture
def photo(db, tmp_path, settings):
    """A saved model instance whose image field is a ThumbnailerImageFieldFile."""
    settings.MEDIA_ROOT = str(tmp_path)

    from django.core.files.base import ContentFile
    from tests.models import Photo

    buf = io.BytesIO()
    Image.new("RGB", (300, 300), "blue").save(buf, format="JPEG")

    photo = Photo()
    photo.image.save("example.jpg", ContentFile(buf.getvalue()), save=False)
    return photo


def test_public_api_exports():
    from easy_thumbnails_rest import serializers

    assert set(serializers.__all__) == {
        "ThumbnailerSerializer",
        "ThumbnailerListSerializer",
        "ThumbnailerJSONSerializer",
    }


def test_version_string():
    import easy_thumbnails_rest

    assert isinstance(easy_thumbnails_rest.__version__, str)


def test_thumbnailer_serializer_returns_alias_url(photo):
    from easy_thumbnails_rest.serializers import ThumbnailerSerializer

    field = ThumbnailerSerializer(alias="avatar")
    field._context = {"request": _build_request()}
    url = field.to_representation(photo.image)
    assert isinstance(url, str)
    assert url.startswith("http://")
    # 'avatar' alias is 50x50 crop; easy-thumbnails encodes that in the filename.
    assert "50x50" in url


def test_list_serializer_returns_all_urls(photo):
    from easy_thumbnails_rest.serializers import ThumbnailerListSerializer

    field = ThumbnailerListSerializer(alias="tests.Photo.image")
    field._context = {"request": _build_request()}
    urls = field.to_representation(photo.image)
    assert isinstance(urls, list)
    # original + small + large
    assert len(urls) == 3
    assert all(u.startswith("http://") for u in urls)


def test_json_serializer_returns_size_map(photo):
    from easy_thumbnails_rest.serializers import ThumbnailerJSONSerializer

    field = ThumbnailerJSONSerializer(alias="tests.Photo.image")
    field._context = {"request": _build_request()}
    data = field.to_representation(photo.image)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"original", "small", "large"}
    assert all(v.startswith("http://") for v in data.values())


def test_empty_value_returns_empty_containers():
    from easy_thumbnails_rest.serializers import (
        ThumbnailerJSONSerializer,
        ThumbnailerListSerializer,
    )

    list_field = ThumbnailerListSerializer(alias="tests.Photo.image")
    list_field._context = {"request": _build_request()}
    assert list_field.to_representation(None) == []

    json_field = ThumbnailerJSONSerializer(alias="tests.Photo.image")
    json_field._context = {"request": _build_request()}
    assert json_field.to_representation(None) == {}
