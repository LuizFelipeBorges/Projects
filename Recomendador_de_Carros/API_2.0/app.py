import os.path
from flask import Flask, request
import os
import json
import run_backend
import get_data
import ml_utils

import sqlite3 as sql

import time

app = Flask(__name__)

def get_predictions():

    videos = []
    
    with sql.connect(run_backend.db_name) as conn:
        c = conn.cursor()
        for line in c.execute("SELECT * FROM infos"):
            line_json = {"modelo": line[0], "link": line[1], "score": line[2]}
            videos.append(line_json)

    predictions = []
    for video in videos:
        predictions.append((video['link'], video['modelo'], float(video['score'])))

    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:25]


    predictions_formatted = []
    for e in predictions:
        predictions_formatted.append("<tr><th><a href=\"{link}\">{modelo}</a></th><th>{score}</th></tr>".format(modelo=e[1], link=e[0], score=e[2]))
  
    return '\n'.join(predictions_formatted)

@app.route('/')
def main_page():
    preds = get_predictions()
    return """<head><h1>Recomendador de Carros</h1></head>
    <body>
    <table>
             {}
    </table>
    </body>""".format(preds)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')