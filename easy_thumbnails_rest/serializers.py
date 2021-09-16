from django.conf import settings
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from rest_framework.serializers import ImageField as ApiImageField
from easy_thumbnails.files import ThumbnailerImageFieldFile, get_thumbnailer

__all__ = ('ThumbnailerSerializer', 'ThumbnailerListSerializer',
           'ThumbnailerJSONSerializer')

THUMBNAIL_ALIASES = getattr(settings, 'THUMBNAIL_ALIASES', {})


def get_url(request, instance, alias=None):
    if alias is not None:
        if isinstance(instance, ThumbnailerImageFieldFile):
            try:
                return request.build_absolute_uri(instance[alias].url)
            except ValueError:
                return request.build_absolute_uri(
                    get_thumbnailer(instance)[alias].url
                )
        elif isinstance(instance, ImageField) \
                or isinstance(instance, ImageFieldFile):
            return request.build_absolute_uri(
                get_thumbnailer(instance)[alias].url
            )
    elif alias is None:
        return request.build_absolute_uri(instance.url)
    else:
        raise TypeError('Unsupported field type')


def image_sizes(request, instance, alias_obj, alias_key):
    if alias_key not in alias_obj:
        raise KeyError(
            'Key %s not found in dict thumbnail aliases' % alias_key)
    i_sizes = list(alias_obj[alias_key].keys())
    return {
        'original': get_url(request, instance),
        **{k: get_url(request, instance, k) for k in i_sizes}
    }


class ThumbnailerSerializer(ApiImageField):

    '''ThumbnailerSerializer

    You can use ThumbnailerSerializer to get image's predefined alias.
    You need to pass argument alias with value as one of the aliases name
    defined in THUMBNAIL_ALIASES
    '''

    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        super(ThumbnailerSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if instance and (self.alias or self.alias == ''):
            return get_url(self.context['request'], instance, self.alias)
        return super().to_representation(instance)


class ThumbnailerListSerializer(ApiImageField):

    '''ThumbnailerListSerializer

    You can use ThumbnailerListSerializer to get image's predefined alias image
    list. You need to pass argument alias with value as one of the target's in
    THUMBNAIL_ALIASES.
    '''

    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        self.alias_obj = kwargs.pop('alias_obj', THUMBNAIL_ALIASES)
        super(ThumbnailerListSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if instance and (self.alias or self.alias == ''):
            return list(
                image_sizes(
                    self.context['request'], instance,
                    self.alias_obj, self.alias
                ).values()
            )
        return []


class ThumbnailerJSONSerializer(ApiImageField):

    '''ThumbnailerJSONSerializer

    You can use ThumbnailerJSONSerializer to get image's predefined alias image
    list. You need to pass argument alias with value as one of the target's in
    THUMBNAIL_ALIASES.
    '''

    def __init__(self, **kwargs):
        self.alias = kwargs.pop('alias', None)
        self.alias_obj = kwargs.pop('alias_obj', THUMBNAIL_ALIASES)
        super(ThumbnailerJSONSerializer, self).__init__(**kwargs)

    def to_representation(self, instance):
        if instance and (self.alias or self.alias == ''):
            return image_sizes(
                self.context['request'], instance,
                self.alias_obj, self.alias
            )
        return {}
