import os

from werkzeug.exceptions import InternalServerError

import app.logging.logging_config as logging_config
import app.simulation.simulation_runner as simulation_runner
from app.exception.app_exception import AppException
import logging

from flask import Flask

log = logging.getLogger('Main')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/status')
    def health_check():
        return 'Alive'

    @app.route('/simulation/start')
    def start_simulation():
        simulation_runner.run_simulation()
        return 'Started'

    @app.route('/simulation/stop')
    def stop_simulation():
        simulation_runner.stop_simulation()
        return 'Stopping'

    @app.errorhandler(AppException)
    def handle_bad_request(e):
        log.error(e.message)
        return e.message, 400

    @app.errorhandler(InternalServerError)
    def handle_500(e):
        return 'Unknown Exception', 500

    return app


def run():
    logging_config.setup()
    app = create_app()
    app.run(host='0.0.0.0')