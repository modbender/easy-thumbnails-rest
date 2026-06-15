---
title: Basic
description: A minimal end-to-end example — define an alias, use ThumbnailerImageField on a model, add ThumbnailerSerializer to a serializer, and serve a single thumbnail URL.
sidebar:
  order: 1
---

The smallest complete setup: one alias, one model field, one serializer field, and a viewset that returns a single thumbnail URL.

## 1. Define a thumbnail alias

In `settings.py`, register a non-targeted `avatar` alias under the empty-string key so any image field can use it:

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'easy_thumbnails',
    'rest_framework',
]

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}
```

## 2. Use ThumbnailerImageField on your model

Use easy-thumbnails' `ThumbnailerImageField` so the field knows how to produce thumbnails:

```python
# models.py
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = ThumbnailerImageField(upload_to='photos')
```

## 3. Add the serializer field

Point `ThumbnailerSerializer` at the `avatar` alias name:

```python
# serializers.py
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    image = ThumbnailerSerializer(alias='avatar')

    class Meta:
        model = Profile
        fields = ['id', 'name', 'image']
```

## 4. Serve it from a viewset

A standard DRF viewset is all you need — it passes the request into serializer context automatically, so the field can build absolute URLs:

```python
# views.py
from rest_framework import viewsets

from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
```

## 5. The response

A `GET` on a profile returns the `avatar` thumbnail as a single absolute URL:

```json
{
  "id": 1,
  "name": "Ada Lovelace",
  "image": "http://example.com/media/photos/example.jpg.50x50_q85_crop.jpg"
}
```

:::tip
Because the viewset supplies `request` in context for you, there's nothing extra to wire up. If you ever build this serializer by hand outside a view, remember to pass `context={'request': request}`.
:::

## Next steps

- [List & JSON example](/easy-thumbnails-rest/examples/list-and-json/) — return every size under a target as a list and as a keyed map.
- [Configuration](/easy-thumbnails-rest/configuration/) — alias options and the difference between alias names and target keys.
