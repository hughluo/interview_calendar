from flask import Blueprint
import json
from json import JSONDecodeError

api = Blueprint('api', __name__)


def api_encoder(raw_input):
    return json.dumps(raw_input)


def api_decoder(raw_input):
    try:
        r = json.loads(raw_input)
        return r
    except JSONDecodeError:
        return None


from . import candidates, interviewers