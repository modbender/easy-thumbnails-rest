import setuptools

README = open('README.md').read()

setuptools.setup(
    name='easy-thumbnails-rest',
    version='1.1.3',
    url='https://github.com/modbender/easy-thumbnails-rest',
    description='Easy Thumbnails Fields for Django Rest API',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    install_requires=[
        'django>=2.2.24',
        'djangorestframework>=3.11.1',
        'easy-thumbnails>=2.7',
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
