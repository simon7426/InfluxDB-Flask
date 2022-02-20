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
    'version': '0.1.1',
    'description': 'InfluxDB-Flask adds influxdb-client-python support to Flask.',
    'long_description': '\n# InfluxDB-Flask\n\n\n## Introduction\n\nInfluxDB went for a massive change from v1.7 to v2.0. They introduced a\nnew client library\n[influxdb-client-python](https://github.com/influxdata/influxdb-client-python)\nto interact with the InfluxDB v2 API. InfluxDB-Flask adds\ninfluxdb-client-python support to Flask.\n\n**Note: Use this library with InfluxDB 2.x and InfluxDB 1.8+.** For\nconnecting to **InfluxDB 1.7** or earlier instances, use the\n[Flask-InfluxDB](https://github.com/btashton/flask-influxdb) that uses\n[InfluxDB-Python](https://github.com/influxdata/influxdb-python) as\nclient library.\n\nThe API of the **influxdb-client-python** is not the\nbackwards-compatible with the old one - **influxdb-python.**\n\n## Installation\n\nInstall the extension via pip:\n\n    $ pip install influxdb-flask\n\n## Set Up\n\nInfluxdb_client can be accessed via InfluxDB class:\n\n    from flask import Flask\n    from influxdb_flask import InfluxDB\n\n    app = Flask(__name__)\n    influxdb = InfluxDB(app)\n\nDelayed configuration of `InfluxDB` is also supported via **init_app**\nmethod:\n\n    influxdb = InfluxDB()\n\n    app = Flask(__name__)\n    influxdb.init_app()\n\nCurrently `InfluxDB.connection` instance provides the functionality of\n`InfluxDBClient` .\n\nAn included example shows how to write and query data from InfluxDB.\n\n## Configuring InfluxDB-Flask\n\nThe following configuration values can be set for InfluxDB-Flask\nextension:\n```\nINFLUXDB_V2_URL                       InfluxDB server API url. Default is <http://localhost:8086>\nINFLUXDB_V2_ORG                       Organization name (used as a default in query and write API). Default is None\nINFLUXDB_V2_TOKEN                     Authentication token.\nINFLUXDB_V2_TIMEOUT                   HTTP client timeout setting for a request specified in milliseconds. Default is 10s.\nINFLUXDB_V2_VERIFY_SSL                Set this to false to skip verifying SSL certificate when calling API from https server. Default is False.\nINFLUXDB_V2_SSL_CA_CERT               Set this to customize the certificate file to verify the peer. Default is None.\nINFLUXDB_V2_CONNECTION_POOL_MAXSIZE   Number of connections to save that can be reused by urllib3. Default is 10.\nINFLUXDB_V2_AUTH_BASIC                Set this to true to enable basic authentication when talking to a InfluxDB 1.8.x that does not use auth-enabled but is protected by \n                                      a reverse proxy with basic authentication. Default is False.\n```',
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

