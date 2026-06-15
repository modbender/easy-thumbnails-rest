# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0]

### Added

- `pyproject.toml`-based packaging (PEP 621), replacing `setup.py`.
- Test suite (`pytest` + `pytest-django`) covering all three serializer fields.
- GitHub Actions workflow for PyPI publishing via OpenID Connect trusted publishing.
- `__version__` attribute on the `easy_thumbnails_rest` package.

### Changed

- Updated supported versions: Python `>=3.9`, Django `>=4.2`,
  Django REST Framework `>=3.14`, easy-thumbnails `>=2.8`.
- Refreshed trove classifiers (Django 4.2–6.0, Python 3.9–3.13).
- Documentation now lives at https://modbender.in/easy-thumbnails-rest/.

### Removed

- Dropped support for end-of-life Django (2.2, 3.x) and Python (3.5–3.8).
