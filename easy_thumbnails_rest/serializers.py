from django.conf import settings
from rest_framework.serializers import ImageField, ListField, JSONField
from easy_thumbnails.fields import ThumbnailerField, ThumbnailerImageField

__all__ = ('ThumbnailerSerializer', 'ThumbnailerListSerializer', 'ThumbnailerJSONSerializer')

THUMBNAIL_ALIASES = getattr(settings, 'THUMBNAIL_ALIASES', {})

def image_sizes(request, image, alias_obj, alias_key):
    if alias_key not in alias_obj:
        raise KeyError('Key %s not found in dict thumbnail aliases'%alias_key)
    i_sizes = alias_obj[alias_key].keys()
    return {
        'original': request.build_absolute_uri(image.url),
        **{k: request.build_absolute_uri(image[k].url) for k in i_sizes}
    }

class ThumbnailerSerializer(ImageField):
    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', '')
        super(ThumbnailerSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if self.alias:
            return self.context['request'].build_absolute_uri(instance[self.alias].url)
        return super().to_representation(instance)

# class ThumbnailerFilterSerializer(ImageField):
#     def __init__(self, **kwargs):
#         self.alias = kwargs.pop('alias', '')
#         super(ThumbnailerSerializer, self).__init__(**kwargs)
#
#     def to_representation(self, instance):
#         if self.alias:
#             return self.context['request'].build_absolute_uri(instance[self.alias].url)
#         return super().to_representation(instance)

class ThumbnailerListSerializer(ImageField):
    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        self.alias_obj = kwargs.pop('alias_obj', THUMBNAIL_ALIASES)
        super(ThumbnailerListSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if self.alias or self.alias == '':
            return list(image_sizes(self.context['request'], instance, self.alias_obj, self.alias).values())
        return []

class ThumbnailerJSONSerializer(ImageField):
    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        self.alias_obj = kwargs.pop('alias_obj', THUMBNAIL_ALIASES)
        super(ThumbnailerJSONSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if self.alias or self.alias == '':
            return image_sizes(self.context['request'], instance, self.alias_obj, self.alias)
        return {}
