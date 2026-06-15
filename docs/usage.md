---
title: Usage
description: The three Easy Thumbnails REST fields — single URL, list, and JSON map — with example serializers and the exact output shape each produces.
sidebar:
  order: 3
---

Easy Thumbnails REST gives you three serializer fields. All three subclass DRF's `ImageField`, so you use them like any other field on a `ModelSerializer` or `Serializer`. The difference is purely in what they emit: a single URL, a list of URLs, or a `{ alias: url }` map.

## Choosing a field

| Field | Returns | Use when |
| --- | --- | --- |
| `ThumbnailerSerializer` | A single URL string | You need exactly one predefined size — an avatar, a hero image, a card thumbnail. |
| `ThumbnailerListSerializer` | A list of URL strings | You want every size under a target as an ordered list, original first. |
| `ThumbnailerJSONSerializer` | A `{ alias: url }` object | You want every size under a target keyed by name, so the client can pick by alias. |

The key difference in arguments: `ThumbnailerSerializer` takes an **alias name** (a single entry), while the List and JSON fields take a **target key** (a whole group of aliases). See [Configuration](/easy-thumbnails-rest/configuration/) for how aliases and targets are structured in `THUMBNAIL_ALIASES`.

## ThumbnailerSerializer

Serializes the image to a single absolute URL for one predefined alias. Pass the alias **name** as `alias`.

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerSerializer


class ProfileSerializer(serializers.ModelSerializer):
    image = ThumbnailerSerializer(alias='avatar')

    class Meta:
        model = Profile
        fields = ['id', 'image']
```

Output:

```json
{
  "id": 1,
  "image": "http://example.com/media/photos/example.jpg.50x50_q85_crop.jpg"
}
```

If the field value is empty (no image set, or no alias resolves), it falls back to DRF's standard `ImageField` representation — the plain image URL, or `null` when the field is empty.

## ThumbnailerListSerializer

Serializes the image to a **list** of absolute URLs: the original image first, followed by one URL per alias defined under the given target. Pass the **target key** as `alias`.

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerListSerializer


class PhotoSerializer(serializers.ModelSerializer):
    image = ThumbnailerListSerializer(alias='gallery.Photo.image')

    class Meta:
        model = Photo
        fields = ['id', 'image']
```

Given a target with `small` and `large` aliases, the output is:

```json
{
  "id": 1,
  "image": [
    "http://example.com/media/photos/example.jpg",
    "http://example.com/media/photos/example.jpg.40x40_q85_crop.jpg",
    "http://example.com/media/photos/example.jpg.200x200_q85_crop.jpg"
  ]
}
```

The **first element is always the original** image URL. When the field value is empty, the field returns an empty list `[]`.

## ThumbnailerJSONSerializer

Same inputs as the List field, but returns a **dict** keyed by alias name, with an `original` key for the source image. Pass the **target key** as `alias`.

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerJSONSerializer


class PhotoSerializer(serializers.ModelSerializer):
    image = ThumbnailerJSONSerializer(alias='gallery.Photo.image')

    class Meta:
        model = Photo
        fields = ['id', 'image']
```

Output for the same `small` + `large` target:

```json
{
  "id": 1,
  "image": {
    "original": "http://example.com/media/photos/example.jpg",
    "small": "http://example.com/media/photos/example.jpg.40x40_q85_crop.jpg",
    "large": "http://example.com/media/photos/example.jpg.200x200_q85_crop.jpg"
  }
}
```

When the field value is empty, the field returns an empty object `{}`.

## Overriding the alias source

The List and JSON fields accept an optional `alias_obj` argument — a dict in the same shape as `THUMBNAIL_ALIASES`. It defaults to `settings.THUMBNAIL_ALIASES`, but you can pass your own dict to resolve aliases from somewhere other than the global setting:

```python
CUSTOM_ALIASES = {
    'thumbnails': {
        'small': {'size': (40, 40), 'crop': True},
        'large': {'size': (200, 200), 'crop': True},
    },
}


class PhotoSerializer(serializers.ModelSerializer):
    image = ThumbnailerListSerializer(alias='thumbnails', alias_obj=CUSTOM_ALIASES)

    class Meta:
        model = Photo
        fields = ['id', 'image']
```

`ThumbnailerSerializer` does not take `alias_obj` — it resolves a single alias name directly through easy-thumbnails.

:::caution
All three fields build absolute URLs and therefore need the request in serializer context. DRF generic views and viewsets supply it automatically; for a bare serializer you must pass `context={'request': request}`. See [Installation](/easy-thumbnails-rest/installation/).
:::

## Next steps

- [Configuration](/easy-thumbnails-rest/configuration/) — structure `THUMBNAIL_ALIASES`, alias options, and `alias_obj`.
- [Basic example](/easy-thumbnails-rest/examples/basic/) — a complete model → serializer → viewset walkthrough.
- [List & JSON example](/easy-thumbnails-rest/examples/list-and-json/) — multi-size output, side by side.
