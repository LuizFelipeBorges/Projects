import os.path
from flask import Flask
import os
import json
import run_backend

import time

app = Flask(__name__)

def get_predictions():

    videos = []
    
    novos_videos_json = "novos_videos.json"
    if not os.path.exists(novos_videos_json):
        run_backend.update_db()

    with open("novos_videos.json", 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
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