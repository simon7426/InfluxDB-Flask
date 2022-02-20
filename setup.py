# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['influxdb_flask']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.3,<3.0.0', 'influxdb-client>=1.25.0,<2.0.0']

setup_kwargs = {
    'name': 'influxdb-flask',
    'version': '0.1.0',
    'description': 'InfluxDB-Flask adds influxdb-client-python support to Flask.',
    'author': 'simon.islam',
    'author_email': 'mail@simonislam.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simon7426/InfluxDB-Flask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

