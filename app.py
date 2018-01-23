import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.lib import Config


app = Flask(__name__)
CORS(app)
app.debug = True
APP_PATH = app.root_path + '/'
CFG = Config(APP_PATH+'config.yml').cfg


@app.route('/ask', methods=['GET', 'POST'])
def answer():
    """
    answer the given question
    :return: json file containing the answers of the given question
    """
    question = request.data

    # build chunks, keywords
    # chunks_keywords = get_chuncks_keywords(question)

    # entity linking
    # entity_linked = get_linked_entity(question)

    # get answer
    # possible_answers = get_answers(question, chunks_keywords, entity_linked)

    # results
    result = dict()
    result['answer'] = 'possible_answers'

    return jsonify(result)


if __name__ == '__main__':
    """
    configure the ip and port where the application should run on
    """
    # run application
    handler = RotatingFileHandler(APP_PATH+CFG['log_path'])
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host=CFG['server']['host'], port=CFG['server']['port'])
