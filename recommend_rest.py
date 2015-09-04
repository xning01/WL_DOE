from flask import Flask, request, jsonify, abort, redirect, url_for
import student_recommend as sRec

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

customerDB = {}  # This should be put into data base finally.
app = Flask(__name__)


@app.route("/")
def index():
    """ GET Index
        Showing that the application is ready
    """
    return jsonify(msg="It's Working! Go ahead!")


@app.route("/newUser", methods=['POST'])
def new_user():
    """ POST a new user
        Adding a new user and initialize the HMMobj
        HowTo use: curl -i -H "Content-Type: application/json" \
               -X POST -d '{"id":1}' http://localhost:5000/id
    """
    if not request.json or not ('id' in request.json):
        abort(400)

    uId = int(request.json['id'])
    if uId in customerDB:
        abort(400)

    user = sRec.User()

    # user = None  # debug
    customerDB[uId] = [False, None, user]
    # post a first question
    return jsonify({"next_question": str(user.sel_first_question())})
    # return jsonify({"next_question": str(111)})


@app.route("/answer", methods=['POST'])
def user_answer():
    """ POST a new user
        Adding a new user and initialize the HMMobj
        HowTo use: curl -i -H "Content-Type: application/json" \
               -X POST -d '{"id":1}' http://localhost:5000/id
    """
    if not request.json or not ('id' in request.json):
        abort(400)
    content = request.json
    uId = int(content['id'])

    print uId

    if not (uId in customerDB):  # redirects to registration page
        return redirect(url_for('new_user'), 301)

    if not ('correctness' in request.json):
        abort(400)

    correctness = int(content['correctness'])
    if correctness != 0:
        correctness = 1

    return jsonify({"next_question":
                    str(customerDB[id][2].get_next_question(correctness))})

    # debug
    # return jsonify({"next_question": "666"})

if __name__ == '__main__':
    """ Main
    """
    app.run(debug=True)
