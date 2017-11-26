#!bam/bin/python

from flask import Flask
from flask import jsonify
import mysql.connector as mariadb
from classes.score import Score

app = Flask(__name__)

connection = mariadb.connect(host='localhost', user='root', password='changeme', database='gallica')
cursor = connection.cursor()

@app.route("/score/all")
def score():
    score = Score(cursor)
    return jsonify(score.get_all())

@app.route("/score/<id>")
def score_id(id):
    score = Score(cursor)
    return jsonify(score.get_byid(id))

@app.route("/search/<q>")
def search(q):
    score = Score(cursor)
    return jsonify(score.search(q))
