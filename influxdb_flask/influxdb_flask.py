import influxdb_client
from flask import Flask, _app_ctx_stack, current_app
from flask.globals import _app_ctx_err_msg

_no_influx_msg = """\
InfluxDB connection is not present.
This means that something has overwritten _app_ctx_stack.top.influxdb.
"""


class InfluxDB(object):
    def __init__(self, app: Flask = None) -> None:
        """
        Constructor Class for InfluxDB
        :param app: Flask application
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize influxdb for application
        :param app: Flask Application object
        """
        app.config.setdefault("INFLUXDB_V2_URL", "http://localhost:8086")
        app.config.setdefault("INFLUXDB_V2_ORG", None)
        app.config.setdefault("INFLUXDB_V2_TOKEN", None)
        app.config.setdefault("INFLUXDB_V2_TIMEOUT", 10000)
        app.config.setdefault("INFLUXDB_V2_VERIFY_SSL", False)
        app.config.setdefault("INFLUXDB_V2_SSL_CA_CERT", None)
        app.config.setdefault("INFLUXDB_V2_CONNECTION_POOL_MAXSIZE", 10)
        app.config.setdefault("INFLUXDB_V2_AUTH_BASIC", False)

        app.teardown_appcontext(self.teardown)

    @staticmethod
    def teardown(exception) -> None:
        """
        Method for tearing down influxdb input
        """
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "influxdb") and ctx.influxdb is not None:
            ctx.influxdb.close()

    @staticmethod
    def connect() -> influxdb_client.InfluxDBClient:
        """
        Connect to influxdb v2 using configuration parameters.
        :return: InfluxDBClient object
        """
        return influxdb_client.InfluxDBClient(
            url=current_app.config["INFLUXDB_V2_URL"],
            org=current_app.config["INFLUXDB_V2_ORG"],
            token=current_app.config["INFLUXDB_V2_TOKEN"],
            timeout=current_app.config["INFLUXDB_V2_TIMEOUT"],
            verify_ssl=current_app.config["INFLUXDB_V2_VERIFY_SSL"],
            ssl_ca_cert=current_app.config["INFLUXDB_V2_SSL_CA_CERT"],
            connection_pool_maxsize=current_app.config[
                "INFLUXDB_V2_CONNECTION_POOL_MAXSIZE"
            ],
            auth_basic=current_app.config["INFLUXDB_V2_AUTH_BASIC"],
        )

    @property
    def connection(self) -> influxdb_client.InfluxDBClient:
        """
        InfluxDBClient object
        :return:
        """
        ctx = _app_ctx_stack.top
        if ctx is None:
            raise RuntimeError(_app_ctx_err_msg)
        if not hasattr(ctx, "influxdb"):
            ctx.influxdb = self.connect()
        if ctx.influxdb is None:
            raise RuntimeError(_no_influx_msg)

        return ctx.influxdb

    @property
    def close(self) -> callable:
        return self.connection.close

    @property
    def buckets_api(self) -> callable:
        return self.connection.buckets_api

    @property
    def authorizations_api(self) -> callable:
        return self.connection.authorizations_api

    @property
    def delete_api(self) -> callable:
        return self.connection.delete_api

    @property
    def health(self) -> callable:
        return self.connection.health

    @property
    def labels_api(self) -> callable:
        return self.connection.labels_api

    @property
    def organizations_api(self) -> callable:
        return self.connection.organizations_api

    @property
    def ping(self) -> callable:
        return self.connection.ping

    @property
    def query_api(self) -> callable:
        return self.connection.query_api

    @property
    def ready(self) -> callable:
        return self.connection.ready

    @property
    def tasks_api(self) -> callable:
        return self.connection.tasks_api

    @property
    def users_api(self) -> callable:
        return self.connection.users_api

    @property
    def version(self) -> callable:
        return self.connection.version

    @property
    def write_api(self) -> callable:
        return self.connection.write_api
