from flask import Flask, request, jsonify, abort, redirect, url_for
import student_recommend as sRec
import score_function as score

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
scoreStat = score.init_stat()  # This is the score stats (global)
thres = 60  # Maximum no of questions a customer can answer

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
               -X POST -d '{"id":1}' http://localhost:5000/newUser
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
    """ POST the answer of a user
        Adding a new user and initialize the HMMobj
        HowTo use: curl -i -H "Content-Type: application/json" \
                     -X POST -d '{"id":1, "correctness": 1}' \
                    http://localhost:5000/answer

                 : curl -i -H "Content-Type: application/json" \
                     -X POST -d '{"id:1", "listLen": 5, "correctness": 0}' \
                    http://localhost:5000/answer
    """
    if not request.json or not ('id' in request.json):
        abort(400)
    content = request.json
    uId = int(content['id'])

    if not (uId in customerDB):  # redirects to registration page
        return redirect(url_for('new_user'), 301)

    if not ('correctness' in request.json):
        abort(400)

    correctness = int(content['correctness'])
    if correctness != 0:
        correctness = 1

    if ('listLen' in request.json):
        listLen = int(content['listLen'])
        return jsonify({"next_list_question":
                        str(customerDB[uId][2].get_list_question(correctness,
                                                                 thres,
                                                                 listLen))})
    else:
        return jsonify({"next_question":
                        str(customerDB[uId][2].get_next_question(correctness,
                                                                 thres))})


@app.route("/score", methods=['POST'])
def get_score():
    """ POST a list of performance to get score
        Getting the score of a batch of answers
        HowTo use: curl -i -H "Content-Type: application/json" \
                        -X POST -d '{"id":1, "accuracy": [1,0,1,0,1]}' \
                        http://localhost:5000/score
                 : curl -i -H "Content-Type: application/json" \
                        -X POST -d '{"id":1, "time": [15, 25, 30, 100]}'
                 Note: time is in terms of millisecond  (1 = 0.001 sec)
    """
    if not request.json or not ('id' in request.json):
        abort(400);

if __name__ == '__main__':
    """ Main
    """
    app.run(debug=True)
