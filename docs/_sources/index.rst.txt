InfluxDB-Flask
===============

.. module:: influxdb_flask

Introduction
------------

InfluxDB went for a massive change from v1.7 to v2.0. They introduced a new client library `influxdb-client-python <https://github.com/influxdata/influxdb-client-python>`_ to interact with the InfluxDB v2 API. InfluxDB-Flask adds influxdb-client-python support to Flask.

**Note: Use this library with InfluxDB 2.x and InfluxDB 1.8+.** For connecting to **InfluxDB 1.7** or earlier instances, use the `Flask-InfluxDB <https://github.com/btashton/flask-influxdb>`_ that uses `InfluxDB-Python <https://github.com/influxdata/influxdb-python>`_ as client library.

The API of the **influxdb-client-python** is not the backwards-compatible with the old one - **influxdb-python.**

Installation
------------

Install the extension via pip::

   $ pip install influxdb-flask

Set Up
------

Influxdb_client can be accessed via InfluxDB class::

   from flask import Flask
   from influxdb_flask import InfluxDB

   app = Flask(__name__)
   influxdb = InfluxDB(app)

Delayed configuration of ``InfluxDB`` is also supported via **init_app** method::

   influxdb = InfluxDB()

   app = Flask(__name__)
   influxdb.init_app()

Currently ``InfluxDB.connection`` instance provides the functionality of ``InfluxDBClient`` .

An included example shows how to write and query data from InfluxDB.

Configuring InfluxDB-Flask
---------------------------

The following configuration values can be set for InfluxDB-Flask extension:

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

======================================= =================================================================================================================================================================================================
``INFLUXDB_V2_URL``                     InfluxDB server API url. Default is http://localhost:8086
``INFLUXDB_V2_ORG``                     Organization name (used as a default in query and write API). Default is None
``INFLUXDB_V2_TOKEN``                   Authentication token
``INFLUXDB_V2_TIMEOUT``                 HTTP client timeout setting for a request specified in milliseconds. Default is 10s. 
``INFLUXDB_V2_VERIFY_SSL``              Set this to false to skip verifying SSL certificate when calling API from https server. Default is False
``INFLUXDB_V2_SSL_CA_CERT``             Set this to customize the certificate file to verify the peer. Default is None.
``INFLUXDB_V2_CONNECTION_POOL_MAXSIZE`` Number of connections to save that can be reused by urllib3. Default is 10.
``INFLUXDB_V2_AUTH_BASIC``              Set this to true to enable basic authentication when talking to a InfluxDB 1.8.x that does not use auth-enabled but is protected by a reverse proxy with basic authentication. Default is False.
======================================= =================================================================================================================================================================================================
