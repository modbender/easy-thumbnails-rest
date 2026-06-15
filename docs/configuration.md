---
title: Configuration
description: How THUMBNAIL_ALIASES maps to each field, the common alias options, choosing single vs list vs JSON output, and the alias_obj override.
sidebar:
  order: 4
---

There's no configuration specific to Easy Thumbnails REST — it reads the `THUMBNAIL_ALIASES` setting you already define for easy-thumbnails. This page covers how that setting maps to each field, and the one override the fields offer.

## THUMBNAIL_ALIASES structure

`THUMBNAIL_ALIASES` is a dict keyed by **target**. Each target holds a group of named aliases, and each alias maps to a dict of thumbnail options.

```python
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
    'gallery.Photo.image': {
        'small': {'size': (40, 40), 'crop': True},
        'large': {'size': (200, 200), 'crop': True},
    },
}
```

### Targeted vs non-targeted aliases

- **The empty-string key `''`** holds *non-targeted* aliases — they're available to every image field in your project. In the example above, `avatar` can be used on any thumbnail field.
- **A specific key like `'gallery.Photo.image'`** (in `app_label.Model.field` form) holds aliases *scoped* to that one model field. Here, `small` and `large` apply to the `image` field on the `Photo` model in the `gallery` app.

See the easy-thumbnails [thumbnail aliases docs](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases) for the full details on targeting.

## How fields reference aliases

This is the one rule worth internalizing:

| Field | `alias` argument refers to | Example |
| --- | --- | --- |
| `ThumbnailerSerializer` | An alias **name** (a single entry) | `alias='avatar'` |
| `ThumbnailerListSerializer` | A **target key** (the whole group) | `alias='gallery.Photo.image'` |
| `ThumbnailerJSONSerializer` | A **target key** (the whole group) | `alias='gallery.Photo.image'` |

So the single-URL field picks one named alias, while the List and JSON fields expand an entire target group — emitting every alias under it plus the original image.

## Alias options

Each alias maps to a dict of thumbnail options. The most common ones:

| Option | Type | Description |
| --- | --- | --- |
| `size` | `(width, height)` tuple | Target dimensions. A `0` for either dimension lets that side scale freely to preserve aspect ratio. |
| `crop` | `bool` or string | Crop to exactly fill `size`. `True` crops from the center; values like `'smart'` or `'10,20'` control the focal point. |
| `quality` | `int` | JPEG quality, `1`–`100`. Defaults to easy-thumbnails' `THUMBNAIL_QUALITY` (85). |
| `upscale` | `bool` | Allow enlarging images smaller than `size`. Defaults to `False`. |
| `bw` | `bool` | Render in grayscale. |

This is a subset — easy-thumbnails supports more processors and options. See its [thumbnail options reference](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases) for the complete list.

```python
THUMBNAIL_ALIASES = {
    'gallery.Photo.image': {
        'small':  {'size': (40, 40),   'crop': True},
        'large':  {'size': (200, 200), 'crop': 'smart', 'quality': 90},
        'wide':   {'size': (800, 0),   'upscale': False},
    },
}
```

## Choosing single, list, or JSON

The three fields are mutually exclusive per field — pick the output shape your client needs:

- **`ThumbnailerSerializer`** when you need exactly one size. The response value is a plain URL string, which is the simplest thing for a client to consume.
- **`ThumbnailerListSerializer`** when you want all sizes under a target and the client iterates them in order (original first). Good for galleries that render whatever sizes exist.
- **`ThumbnailerJSONSerializer`** when you want all sizes but the client picks a specific one by name (`image.large`, `image.small`). The most self-describing option.

## The `alias_obj` override

The List and JSON fields take an optional `alias_obj` argument: a dict in the same shape as `THUMBNAIL_ALIASES`. It defaults to `settings.THUMBNAIL_ALIASES`, but you can supply a different dict to resolve aliases from somewhere other than the global setting — useful when one serializer needs a bespoke set of sizes that don't belong in project-wide settings.

```python
PHOTO_SIZES = {
    'detail': {
        'thumb': {'size': (60, 60),  'crop': True},
        'full':  {'size': (1200, 0), 'upscale': False},
    },
}


class PhotoDetailSerializer(serializers.ModelSerializer):
    image = ThumbnailerJSONSerializer(alias='detail', alias_obj=PHOTO_SIZES)

    class Meta:
        model = Photo
        fields = ['id', 'image']
```

:::note
`ThumbnailerSerializer` does not accept `alias_obj` — it resolves a single alias name through easy-thumbnails directly, so the override only applies to the List and JSON fields.
:::

## Next steps

- [Usage](/easy-thumbnails-rest/usage/) — the three fields and their exact output shapes.
- [Basic example](/easy-thumbnails-rest/examples/basic/) — a single-URL setup, end to end.
- [List & JSON example](/easy-thumbnails-rest/examples/list-and-json/) — multi-size output with both fields.
