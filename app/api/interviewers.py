from flask import request
from app.models.interviewer import Interviewer
from app.api import api, api_encoder
from app.api.error import bad_request
from utils import is_slot_legal, log


@api.route("/interviewers/<int:iid>/slots", methods=["POST"])
def add_slot_i(iid):
    t_from = request.args.get('t_from', -1)
    t_to = request.args.get('t_to', -1)
    if Interviewer.check_existence_by_id(iid):
        if is_slot_legal(t_from, t_to):
            t_from = int(t_from)
            t_to = int(t_to)
            Interviewer.add_slot_by_id(iid, t_from, t_to)
            slots = Interviewer.get_slots_by_id(iid)
            return api_encoder(slots)
        else:
            return bad_request('Slot is illegal')
    else:
        return bad_request('Interviewer not exists')

