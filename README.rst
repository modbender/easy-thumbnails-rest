Easy Thumbnails Rest
====================

Easy Thumbnails Fields for Django Rest API Framework

Installation
------------

| Run ``pip install easy-thumbnails-rest``
| Add ``easy_thumbnails_rest`` to INSTALLED\_APPS

::

    INSTALLED_APPS = (
      ...
      'easy_thumbnails',
      'easy_thumbnails_rest'
    )

Usage
-----

| Remember that this app needs ``THUMBNAIL_ALIASES`` to be defined in
``settings.py`` to work.
| If not yet added, please check `Easy Thumbnails
Docs <https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases>`__
to add it.
| Example settings.THUMBNAIL\_ALIASES

::

    THUMBNAIL_ALIASES = {
        '': {
            'avatar': {'size': (50, 50), 'crop': True},
        },
    }

Fields:
~~~~~~~

-  ThumbnailerField
-  ThumbnailerListField

ThumbnailerField
^^^^^^^^^^^^^^^^

You can use ``ThumbnailerField`` to get image's predefined alias. You
need to pass argument ``alias`` with value as one of the aliases name
defined in ``THUMBNAIL_ALIASES``

Example:

::

    from rest_framework import serializers
    from easy_thumbnails_rest.fields import ThumbnailerField

    class ExampleSerializer(serializers.ModelSerializer):
        image = ThumbnailerField(alias='avatar')

        class Meta:
            model = ExampleModel
            fields = '__all__'

From the above example the field ``image`` will contain string value of
alias image url.

ThumbnailerListField
~~~~~~~~~~~~~~~~~~~~

| You can use ``ThumbnailerListField`` to get image's predefined alias
values list. You need to pass argument ``alias`` with value as one of
the target's in ``THUMBNAIL_ALIASES``
| If you don't understand where to find target, please see the structure
of the ``THUMBNAIL_ALIASES`` in `Easy Thumbnails
Docs <https://easy-thumbnails.readthedocs.io/en/latest/usage/#thumbnail-aliases>`__

Example:

::

    from rest_framework import serializers
    from easy_thumbnails_rest.fields import ThumbnailerListField

    class ExampleSerializer(serializers.ModelSerializer):
        image = ThumbnailerListField(alias='')

        class Meta:
            model = ExampleModel
            fields = '__all__'

From the above example the field ``image`` will contain JSON value
having all aliased image urls under a target.
