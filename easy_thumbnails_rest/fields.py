from django.conf import settings
from rest_framework.serializers import ImageField, JSONField

__all__ = ('ThumbnailerField', 'ThumbnailerListField')

THUMBNAIL_ALIASES = getattr(settings, 'THUMBNAIL_ALIASES', {})

def image_sizes(request, image, alias_obj, alias_key):
    if alias_key not in alias_obj:
        raise KeyError('Key %s not found in dict thumbnail aliases'%alias_key)
    i_sizes = alias_obj[alias_key].keys()
    return {
        **{k: request.build_absolute_uri(image[k].url) for k in i_sizes},
        'original': request.build_absolute_uri(image.url)
    }

class ThumbnailerField(ImageField):
    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', '')
        super(ThumbnailerField, self).__init__(**kwargs)

    def to_representation(self, instance):
        if self.alias:
            return self.context['request'].build_absolute_uri(instance[self.alias].url)
        return super().to_representation(instance)

class ThumbnailerListField(JSONField):
    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        self.alias_obj = kwargs.pop('alias_obj', THUMBNAIL_ALIASES)
        super(ThumbnailerListField, self).__init__(**kwargs)

    def to_representation(self, instance):
        if self.alias or self.alias == '':
            return image_sizes(self.context['request'], instance, self.alias_obj, self.alias)
        return {}
