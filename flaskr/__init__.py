import os

from flask import Flask, request, jsonify


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

    # a simple page that says hello
    @app.route('/hello',)
    def hello():

        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


##################TEST @ Parallel dot#####################################################

    quarks = [{'name': 'up', 'charge': '+2/3'},
              {'name': 'down', 'charge': '-1/3'},
              {'name': 'charm', 'charge': '+2/3'},
              {'name': 'strange', 'charge': '-1/3'}]

    @app.route('/', methods=['GET'])
    def hello_world():
        return jsonify({'message': 'Hello, World!'})

    @app.route('/quarks', methods=['GET'])
    def returnAll():
        return jsonify({'quarks': quarks})

    @app.route('/quarks/<string:name>', methods=['GET'])
    def returnOne(name):
        theOne = quarks[0]
        for i, q in enumerate(quarks):
            if q['name'] == name:
                theOne = quarks[i]
        return jsonify({'quarks': theOne})

    @app.route('/quarks', methods=['POST'])
    def addOne():
        new_quark = request.get_json()
        quarks.append(new_quark)
        return jsonify({'quarks': quarks})

    @app.route('/quarks/<string:name>', methods=['PUT'])
    def editOne(name):
        new_quark = request.get_json()
        for i, q in enumerate(quarks):
            if q['name'] == name:
                quarks[i] = new_quark
        qs = request.get_json()
        return jsonify({'quarks': quarks})

    @app.route('/quarks/<string:name>', methods=['DELETE'])
    def deleteOne(name):
        for i, q in enumerate(quarks):
            if q['name'] == name:
                del quarks[i]
        return jsonify({'quarks': quarks})

#####################################################################


    


    return app

##########TO RUN USE THIN ##########
####REFER : http://flask.pocoo.org/docs/1.0/tutorial/factory/
# export FLASK_APP=flaskr
# export FLASK_ENV = development
# flask run