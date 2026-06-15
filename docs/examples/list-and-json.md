---
title: List & JSON
description: Return every thumbnail size under a target — as an ordered list with ThumbnailerListSerializer, and as a keyed map with ThumbnailerJSONSerializer.
sidebar:
  order: 2
---

When you want more than one size, point the List or JSON field at a **target key** that groups several aliases. Both fields expand the whole group; they differ only in output shape — an ordered list versus a name-keyed map.

## 1. Define a targeted alias group

This time, scope a group of sizes to a specific model field using its `app_label.Model.field` key:

```python
# settings.py
THUMBNAIL_ALIASES = {
    'gallery.Photo.image': {
        'small': {'size': (40, 40),   'crop': True},
        'large': {'size': (200, 200), 'crop': True},
    },
}
```

## 2. The model

```python
# gallery/models.py
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Photo(models.Model):
    image = ThumbnailerImageField(upload_to='photos')
```

## 3. Two serializers, two shapes

Both fields take the **target key** (`'gallery.Photo.image'`) as `alias`:

```python
# gallery/serializers.py
from rest_framework import serializers
from easy_thumbnails_rest.serializers import (
    ThumbnailerListSerializer,
    ThumbnailerJSONSerializer,
)

from .models import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    image = ThumbnailerListSerializer(alias='gallery.Photo.image')

    class Meta:
        model = Photo
        fields = ['id', 'image']


class PhotoJSONSerializer(serializers.ModelSerializer):
    image = ThumbnailerJSONSerializer(alias='gallery.Photo.image')

    class Meta:
        model = Photo
        fields = ['id', 'image']
```

## 4. The two output shapes

`ThumbnailerListSerializer` returns an **ordered list**, with the original image first:

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

`ThumbnailerJSONSerializer` returns a **keyed map**, with an `original` entry plus one entry per alias:

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

## When to pick each

- **List** when the client just renders whatever sizes exist, in order — a gallery, a `srcset`-style loop. It doesn't need to know the alias names.
- **JSON** when the client selects a specific size by name (`image.small`, `image.large`). It's self-describing and survives reordering or adding sizes without breaking client indexing.

:::tip
Both fields read the same target group, so switching a serializer from list to map output is a one-line change — swap `ThumbnailerListSerializer` for `ThumbnailerJSONSerializer`. The aliases and target stay identical.
:::

:::note
If the image field is empty, the List field returns `[]` and the JSON field returns `{}` — never `null` — so clients can iterate the result without a presence check.
:::

## Next steps

- [Configuration](/easy-thumbnails-rest/configuration/) — alias options and the `alias_obj` override for custom alias dicts.
- [Usage](/easy-thumbnails-rest/usage/) — the full field comparison and the request-context requirement.
