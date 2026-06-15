---
title: Easy Thumbnails REST
description: DRF serializer fields that turn your easy-thumbnails aliases into ready-to-serve thumbnail URLs in your API responses — single URL, list, or JSON map.
sidebar:
  order: 1
---

Serving thumbnails from a Django REST Framework API usually means generating each size by hand, building absolute URLs, and stitching them into your serializer output. Easy Thumbnails REST does that for you.

It's a thin set of DRF serializer fields built on top of the excellent [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails) library. You already define your thumbnail sizes once as `THUMBNAIL_ALIASES` in `settings.py` — these fields read those aliases and emit the matching thumbnail URLs directly in your API responses. No view boilerplate, no manual URL building.

## Key features

- **Three field types, one job each** — `ThumbnailerSerializer` returns a single URL, `ThumbnailerListSerializer` returns a list of URLs, and `ThumbnailerJSONSerializer` returns a `{ alias: url }` map. Pick the shape your client wants.
- **Absolute URLs out of the box** — every URL is built with the request's host, so clients get fully-qualified links they can use as-is.
- **Zero extra config** — there's nothing new to configure beyond the `THUMBNAIL_ALIASES` you already have for easy-thumbnails. The fields reuse it directly.
- **Drop-in DRF fields** — they subclass DRF's `ImageField`, so they work inside any `ModelSerializer`, `Serializer`, viewset, or generic view with no special handling.
- **Broad version support** — Python 3.9+, Django 4.2 through 6.0, and DRF 3.14+.

## A 30-second taste

Define a thumbnail alias in `settings.py` (this is plain easy-thumbnails config):

```python
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}
```

Add the field to a serializer, pointing it at that alias:

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerSerializer


class ProfileSerializer(serializers.ModelSerializer):
    image = ThumbnailerSerializer(alias='avatar')

    class Meta:
        model = Profile
        fields = ['id', 'image']
```

Serve it through a viewset, and the response carries the thumbnail URL:

```json
{
  "id": 1,
  "image": "http://example.com/media/photos/example.jpg.50x50_q85_crop.jpg"
}
```

That's the whole thing. The `image` field now holds the absolute URL of the `avatar` thumbnail instead of the raw image.

## Compatibility

| | Supported |
| --- | --- |
| Easy Thumbnails REST | 1.2.x |
| Python | 3.9+ |
| Django | 4.2+ (4.2 LTS, 5.0, 5.1, 5.2, 6.0) |
| Django REST Framework | 3.14+ |
| easy-thumbnails | 2.8+ |

:::tip
If you've already configured easy-thumbnails in your project, you're most of the way there — these fields read your existing `THUMBNAIL_ALIASES` with nothing extra to set up.
:::

## Where to next

- [Installation](/easy-thumbnails-rest/installation/) — install the package and confirm your prerequisites.
- [Usage](/easy-thumbnails-rest/usage/) — the three fields, what each returns, and when to reach for which.
- [Configuration](/easy-thumbnails-rest/configuration/) — how `THUMBNAIL_ALIASES` maps to each field, plus the `alias_obj` override.
