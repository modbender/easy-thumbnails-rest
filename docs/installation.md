---
title: Installation
description: Install Easy Thumbnails REST, confirm your easy-thumbnails prerequisites, and get the serializer fields ready to use.
sidebar:
  order: 2
---

Getting Easy Thumbnails REST running takes one install plus a quick check that your easy-thumbnails setup is in place. The package depends on `django`, `djangorestframework`, and `easy-thumbnails`, so pip pulls those in for you if they aren't already installed.

## 1. Install the package

```bash
pip install easy-thumbnails-rest
```

That's the only install step. There's no app to add to `INSTALLED_APPS` for this package itself — it just provides serializer fields you import and use.

## 2. Confirm your prerequisites

The fields read your existing easy-thumbnails configuration, so a few things from that library need to be in place first:

- **`easy_thumbnails` is in `INSTALLED_APPS`:**

  ```python
  INSTALLED_APPS = [
      # ...
      'easy_thumbnails',
  ]
  ```

- **Your image fields use easy-thumbnails' `ThumbnailerImageField`** instead of Django's plain `ImageField`:

  ```python
  from django.db import models
  from easy_thumbnails.fields import ThumbnailerImageField


  class Profile(models.Model):
      image = ThumbnailerImageField(upload_to='photos')
  ```

- **`THUMBNAIL_ALIASES` is defined in `settings.py`** with at least one alias:

  ```python
  THUMBNAIL_ALIASES = {
      '': {
          'avatar': {'size': (50, 50), 'crop': True},
      },
  }
  ```

  If you haven't set this up yet, see the easy-thumbnails [thumbnail aliases docs](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases) for the full structure.

## 3. Import the fields

The three fields live in `easy_thumbnails_rest.serializers`:

```python
from easy_thumbnails_rest.serializers import (
    ThumbnailerSerializer,
    ThumbnailerListSerializer,
    ThumbnailerJSONSerializer,
)
```

:::caution
The fields build **absolute** URLs, which means they need the current request in the serializer's context. DRF's generic views and viewsets pass `request` into serializer context automatically, so this works with no effort there. If you instantiate a serializer by hand, you must pass it yourself: `MySerializer(instance, context={'request': request})`. Without it the field raises a `KeyError` on `'request'`.
:::

## Next steps

- [Usage](/easy-thumbnails-rest/usage/) — wire the fields into a serializer and see what each one returns.
- [Configuration](/easy-thumbnails-rest/configuration/) — how `THUMBNAIL_ALIASES` targets and aliases map to each field.
