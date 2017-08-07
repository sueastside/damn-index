from __future__ import absolute_import
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Digital Assets Managed Neatly: Indexing',
    'author': 'sueastside',
    'url': 'https://github.com/peragro/damn-index',
    'download_url': 'https://github.com/peragro/damn-index',
    'author_email': 'No, thanks',
    'version': '0.1',
    'test_suite': 'tests.suite',
    'install_requires': ['damn_at', 'elasticsearch'],
    'test_requires': [],
    'packages': ['damn_index'],
    'scripts': [],
    'name': 'damn_index',
    'entry_points': {
          'peragro.commandline.hooks': [
            'index = damn_index.cli:create_argparse',
          ]
    }
}

setup(**config)
