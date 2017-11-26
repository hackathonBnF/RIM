#!bam/bin/python

from flask import Flask
app = Flask(__name__)

@app.route("/score")
def score():
    return "foo"
