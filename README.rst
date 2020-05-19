====================
Easy Thumbnails Rest
====================

Easy Thumbnails Fields for Django Rest API Framework

Installation
############

Run ``pip install easy-thumbnails-rest``.

**[OPTIONAL]** Add ``easy_thumbnails_rest`` to ``INSTALLED_APPS``

::

    INSTALLED_APPS = (
      ...
      'easy_thumbnails',
      'easy_thumbnails_rest' #optional
    )

Usage
#####

Remember that this app needs ``THUMBNAIL_ALIASES`` to be defined in ``settings.py`` and the field that you need to serialize should be of type ``ThumbnailerImageField`` (or ``ThumbnailerField``) to work.

If not yet added, please check `Easy Thumbnails Docs <https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases>`_ to add it.

Example ``settings.THUMBNAIL_ALIASES``

::

    THUMBNAIL_ALIASES = {
        '': {
            'avatar': {'size': (50, 50), 'crop': True},
        },
    }

Fields:
#######

-  ThumbnailerSerializer
-  ThumbnailerListSerializer

ThumbnailerSerializer
*********************

You can use ``ThumbnailerSerializer`` to get image's predefined alias. You need to pass argument ``alias`` with value as one of the aliases name defined in ``THUMBNAIL_ALIASES``

Example:

::

    from rest_framework import serializers
    from easy_thumbnails_rest.serializers import ThumbnailerSerializer

    class ExampleSerializer(serializers.ModelSerializer):
        image = ThumbnailerSerializer(alias='avatar')

        class Meta:
            model = ExampleModel
            fields = '__all__'

From the above example the field ``image`` will contain string value of alias image url.

ThumbnailerListSerializer
*************************

You can use ``ThumbnailerListSerializer`` to get image's predefined alias values list. You need to pass argument ``alias`` with value as one of the target's in ``THUMBNAIL_ALIASES``.

If you don't understand where to find target, please see the structure of the ``THUMBNAIL_ALIASES`` in `Easy Thumbnails Docs <https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases>`_

Example:

::

    from rest_framework import serializers
    from easy_thumbnails_rest.serializers import ThumbnailerListSerializer

    class ExampleSerializer(serializers.ModelSerializer):
        image = ThumbnailerListSerializer(alias='')

        class Meta:
            model = ExampleModel
            fields = '__all__'

From the above example the field ``image`` will contain JSON value having all aliased image urls under a target.
