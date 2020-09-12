# Easy Thumbnails Rest

[![Downloads](https://pepy.tech/badge/easy-thumbnails-rest)](https://pepy.tech/project/easy-thumbnails-rest)
[![Downloads](https://pepy.tech/badge/easy-thumbnails-rest/month)](https://pepy.tech/project/easy-thumbnails-rest/month)
[![Downloads](https://pepy.tech/badge/easy-thumbnails-rest/week)](https://pepy.tech/project/easy-thumbnails-rest/week)

Easy Thumbnails Fields for Django Rest API Framework

## Installation

`pip install easy-thumbnails-rest`

## Usage
Remember that this app needs `THUMBNAIL_ALIASES` to be defined in `settings.py`

If not yet added, please check [Easy Thumbnails Docs](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases) to add it.

Example `settings.THUMBNAIL_ALIASES`

```python
THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}
```


## Fields

- ThumbnailerSerializer
- ThumbnailerListSerializer
- ThumbnailerJSONSerializer

### ThumbnailerSerializer

You can use `ThumbnailerSerializer` to get image's predefined alias. You need to pass argument `alias` with value as one of the aliases name defined in `THUMBNAIL_ALIASES`

Example:

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerSerializer

class ExampleSerializer(serializers.ModelSerializer):
    image = ThumbnailerSerializer(alias='avatar')

    class Meta:
        model = ExampleModel
        fields = '__all__'
```

From the above example the field `image` will contain string value of alias image url.

### ThumbnailerListSerializer

You can use `ThumbnailerListSerializer` to get image's predefined alias image list. You need to pass argument `alias` with value as one of the target's in `THUMBNAIL_ALIASES`.

If you don't understand where to find target, please see the structure of the `THUMBNAIL_ALIASES` in [Easy Thumbnails Docs](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases)

Example:

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerListSerializer

class ExampleSerializer(serializers.ModelSerializer):
    image = ThumbnailerListSerializer(alias='target')

    class Meta:
        model = ExampleModel
        fields = '__all__'
```

From the above example the field `image` will contain list of all aliased image urls under the given target.

### ThumbnailerJSONSerializer

You can use `ThumbnailerJSONSerializer` to get image's predefined alias image list. You need to pass argument `alias` with value as one of the target's in `THUMBNAIL_ALIASES`.

If you don't understand where to find target, please see the structure of the `THUMBNAIL_ALIASES` in [Easy Thumbnails Docs](https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases)

Example:

```python
from rest_framework import serializers
from easy_thumbnails_rest.serializers import ThumbnailerJSONSerializer

class ExampleSerializer(serializers.ModelSerializer):
    image = ThumbnailerJSONSerializer(alias='target')

    class Meta:
        model = ExampleModel
          fields = '__all__'
```
From the above example the field `image` will contain list of key-value pair where key's are the alias under the given target and values are the respective image url.
