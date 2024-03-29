import os
from datetime import datetime

import influxdb_client
import pytest
from flask import Flask, g
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_flask import __version__
from influxdb_flask.influxdb_flask import InfluxDB, _no_influx_msg

_no_app_msg = """\
Working outside of application context.

This typically means that you attempted to use functionality that needed
the current application. To solve this, set up an application context
with app.app_context(). See the documentation for more information.\
"""


def test_version():
    assert __version__ == "0.1.2"


class TestBase:
    def test_outside_ctx(self, influx):
        with pytest.raises(RuntimeError) as excinfo:
            influx.query_api().query('from(bucket:"test") |> range(start: -10m)')

        assert str(excinfo.value) == _no_app_msg

    def test_overwrite_influxdb(self, app_no_cleanup, influx):
        app = app_no_cleanup

        with app.ctx, pytest.raises(RuntimeError) as excinfo:
            g.influxdb = None
            influx.query_api().query('from(bucket:"test") |> range(start: -10m)')

        assert str(excinfo.value) == _no_influx_msg

    def test_instance(self, app, influx):
        with app.ctx:
            influx.query_api().query('from(bucket:"test") |> range(start: -10m)')

            flux = g.influxdb
        assert isinstance(flux, influxdb_client.InfluxDBClient)

    def test_app_non_factory_pattern(self):
        app = Flask(__name__)
        influx = InfluxDB(app)

        rel_dir = os.path.dirname(__file__)
        config = os.path.join(rel_dir, "config.cfg")

        app.config.from_pyfile(config)

        with app.app_context():
            assert isinstance(influx.connect(), influxdb_client.InfluxDBClient)


class TestAPI:
    def test_base(self, app, influx):
        with app.ctx:
            assert hasattr(influx, "connection")
            assert hasattr(influx, "close")
            assert hasattr(influx, "buckets_api")
            assert hasattr(influx, "authorizations_api")
            assert hasattr(influx, "delete_api")
            assert hasattr(influx, "health")
            assert hasattr(influx, "labels_api")
            assert hasattr(influx, "organizations_api")
            assert hasattr(influx, "ping")
            assert hasattr(influx, "query_api")
            assert hasattr(influx, "ready")
            assert hasattr(influx, "tasks_api")
            assert hasattr(influx, "users_api")
            assert hasattr(influx, "version")
            assert hasattr(influx, "write_api")


class TestTags:
    def test_values(self, app, influx):
        measurement = "test_tags"
        points = [
            {
                "fields": {"index": 1},
                "tags": {"info": "test1"},
                "measurement": measurement,
                "time": datetime.utcnow(),
            },
            {
                "fields": {"index": 2},
                "tags": {"info": "test2"},
                "measurement": measurement,
                "time": datetime.utcnow(),
            },
        ]

        with app.ctx:
            influx.write_api(SYNCHRONOUS).write("test", "test", points[0])
            influx.write_api(SYNCHRONOUS).write("test", "test", points[1])
            result = influx.query_api().query(
                (
                    'from(bucket: "test") |> range(start: -10m) |> filter(fn: (r) => r["info"] == "test1" or'
                    ' r["info"] == "test2") |> aggregateWindow(every: 1m, fn: last, createEmpty: false) |> '
                    'yield(name: "last")'
                )
            )
        assert isinstance(result, list)

        result = list(result)
        assert len(result) == 2
        assert "test1" in result[0].records[0].values["info"]
        assert "test2" in result[1].records[0].values["info"]

    def test_keys(self, app, influx):
        measurement = "test_tags"
        points = [
            {
                "fields": {"index": 1},
                "tags": {"info": "test1"},
                "measurement": measurement,
                "time": datetime.utcnow(),
            },
            {
                "fields": {"index": 2},
                "tags": {"info": "test2"},
                "measurement": measurement,
                "time": datetime.utcnow(),
            },
        ]

        with app.ctx:
            influx.write_api(SYNCHRONOUS).write("test", "test", points[0])
            influx.write_api(SYNCHRONOUS).write("test", "test", points[1])
            result = influx.query_api().query(
                (
                    'from(bucket: "test") |> range(start: -10m) |> '
                    'filter(fn: (r) => r["_measurement"] == "test_tags") |> '
                    'aggregateWindow(every: 1m, fn: last, createEmpty: false) |> yield(name: "last")'
                )
            )
        assert isinstance(result, list)
        assert "info" in result[0].records[0].values
        assert "info" in result[1].records[0].values


class TestApp:
    def test_response(self, app, influx):
        result = app.client.get("/add/dhaka/30")
        assert result.status_code == 200

        with app.ctx:
            result = influx.query_api().query(
                (
                    'from(bucket: "test") |> range(start: -10m) |> '
                    'filter(fn: (r) => r["_measurement"] == "temperature")'
                    ' |> aggregateWindow(every: 1m, fn: last, createEmpty: false) |> yield(name: "last")'
                )
            )
        assert len(result) == 1
        assert result[0].records[0].values["location"] == "dhaka"
        assert result[0].records[0].values["_value"] == "30"
