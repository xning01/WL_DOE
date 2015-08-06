from flask import Flask, request

"""
Initialization 

customerDB: per-customer dict.
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

app: flask rest object.
    provide REST APIs
"""
customerDB = {}
app = Flask(__name__)

"""
    Index message 
    indicating the application is ready
"""
@app.route("/")
def index():
    return "It's Working! Go ahead to try out the recommendation"

"""
    POST message for a new customer
"""
@app.route("/id", methods=['POST'])
def new_customer():
    

if __name__ == '__main__':
    app.run(debug=True)
