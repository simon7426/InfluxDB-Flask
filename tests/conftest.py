from http import client
import os
from collections import namedtuple
from datetime import datetime

import pytest
from flask import Flask, jsonify

from influxdb_flask import InfluxDB
from influxdb_client.client.write_api import SYNCHRONOUS

App = namedtuple("App", ["ctx", "client"])

influxdb = InfluxDB()


def create_app(config: str) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(config)

    influxdb.init_app(app)

    @app.route("/add/<location>/<value>")
    def write(location: str, value: int):
        point = {
            "measurement": "temperature",
            "tags": {"location": location},
            "fields": {"value": value},
            "time": datetime.utcnow(),
        }
        write_api = influxdb.write_api(SYNCHRONOUS)
        result = write_api.write(
            app.config["INFLUXDB_V2_BUCKET"], app.config["INFLUXDB_V2_ORG"], point
        )
        return jsonify(result=result)

    return app


@pytest.fixture(scope="session")
def influx():
    return influxdb


@pytest.fixture()
def app(request):
    """Session wide test application"""
    rel_dir = os.path.dirname(__file__)
    config = os.path.join(rel_dir, "config.cfg")

    app = create_app(config)

    client = app.test_client()
    ctx = app.app_context()

    yield App(ctx, client)



@pytest.fixture()
def app_no_cleanup(request):
    """Session wide test application"""
    rel_dir = os.path.dirname(__file__)
    config = os.path.join(rel_dir, "config.cfg")

    # Create app
    app = create_app(config)

    client = app.test_client()
    ctx = app.app_context()

    yield App(ctx, client)
