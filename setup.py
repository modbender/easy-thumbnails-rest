import setuptools

setuptools.setup(
    name='easy-thumbnails-rest',
    version='1.0',
    url='https://github.com/yashas123/easy-thumbnails-rest',
    description='Easy Thumbnails Fields for Django Rest API',
    long_description='Easy Thumbnails Fields for Django Rest API Framework',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    install_requires=[
        'django',
        'djangorestframework',
        'easy-thumbnails',
    ],
    python_requires='>=3.5',
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
