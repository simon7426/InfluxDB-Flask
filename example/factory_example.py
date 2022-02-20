from datetime import datetime

from flask import Flask, Response, jsonify, make_response
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_flask import InfluxDB

influxdb = InfluxDB()


def create_app(config: str) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("example.cfg")

    influxdb.init_app(app)

    @app.route("/write/<location>/<value>")
    def write(location: str, value: float) -> Response:
        point = {
            "measurement": "temperature",
            "tags": {"location": location},
            "fields": {"value": float(value)},
            "time": datetime.utcnow(),
        }

        write_api = influxdb.write_api(SYNCHRONOUS)
        write_api.write(
            app.config["INFLUXDB_V2_BUCKET"], app.config["INFLUXDB_V2_ORG"], point
        )
        response_obj = {"message": "data written to influxdb"}
        return make_response(jsonify(response_obj)), 201

    @app.route("/read")
    def read() -> Response:
        results = influxdb.query_api().query(
            """from(bucket: "example")\
                |> range(start: -10m)\
                |> filter(fn: (r) => r["_measurement"] == "temperature")\
                |> aggregateWindow(every: 1m, fn: last, createEmpty: false)\
                |> yield(name: "last")"""
        )
        return_object = []
        for result in results:
            for record in result.records:
                return_object.append(record.values)
        return make_response(jsonify(return_object)), 200

    return app


if __name__ == "__main__":
    app = create_app("example.cfg")

    point = {
        "measurement": "temperature",
        "tags": {"location": "dhaka"},
        "fields": {"value": float(30)},
        "time": datetime.utcnow(),
    }

    with app.app_context():
        write_api = influxdb.write_api(SYNCHRONOUS)
        write_api.write(
            app.config["INFLUXDB_V2_BUCKET"], app.config["INFLUXDB_V2_ORG"], point
        )

    app.run()
