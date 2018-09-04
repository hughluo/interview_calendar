from flask import request
from app.models.candidate import Candidate
from app.models.interviewer import Interviewer
from app.api import api, api_encoder, api_decoder
from app.api.error import bad_request
from utils import is_slot_legal, log


@api.route("/candidates/<int:cid>/slots", methods=["POST"])
def add_slot_c(cid):
    t_from = request.args.get('t_from', -1)
    t_to = request.args.get('t_to', -1)
    if Candidate.check_existence_by_id(cid):
        if is_slot_legal(t_from, t_to):
            t_from = int(t_from)
            t_to = int(t_to)
            Candidate.add_slot_by_id(cid, t_from, t_to)
            slots = Candidate.get_slots_by_id(cid)
            return api_encoder(slots)
        else:
            return bad_request('Slot is illegal')
    else:
        return bad_request('Candidate not exists')


@api.route("/candidates/<int:cid>/matching", methods=["GET"])
def get_matching_for_candidate(cid):
    iids_raw = request.args.get('iids', [])
    iids = api_decoder(iids_raw)
    if Candidate.check_existence_by_id(cid):
        if type(iids) is list and len(iids) > 0:
            if Interviewer.check_all_existence_by_id(iids):
                print(cid, iids)
                ms = Candidate.get_matching_by_id(cid, iids)
                print(ms)
                return api_encoder(ms)
    else:
        return bad_request('Candidate not exists')

    return bad_request('Iids is illegal')


