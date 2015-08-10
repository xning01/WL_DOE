from flask import Flask, request, jsonify, abort

""" Initialization
    1. customerDB: per-customer dict.
    key : type int
          unique customer id
    value : type list
            [ready, nextQuestionID, HMMobj]
                ready: bool
                       indicate whether the result is ready
                nextQuestionID: int
                       indicate the id of the next index
                HMMobj:
                       the hidden markov model for each client

    TODO: In multi-machine scenario, the request from a certain
          should always being routed to a same machine

    2. app: flask rest object.
        provide REST APIs
"""

customerDB = {}
app = Flask(__name__)


@app.route("/")
def index():
    """ GET Index
        Showing that the application is ready
    """
    return jsonify(msg="It's Working! Go ahead!")


@app.route("/id", methods=['POST'])
def new_user():
    """ POST a new user
        Adding a new user and initialize the HMMobj
        HowTo use: curl -i -H "Content-Type: application/json" \
               -X POST -d '{"id":1}' http://localhost:5000/id
    """
    if not request.json or not ('id' in request.json):
        abort(400)


@app.route("/id/answer", method=['POST'])
def user_answer():
    """ POST the answer of a customer
    """
    return

if __name__ == '__main__':
    """ Main
    """
    app.run(debug=True)
