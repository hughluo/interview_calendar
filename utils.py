import json
from datetime import datetime

# bunch of time inverters


def datetime2epoch(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds())


def epoch2datetime(et):
    return datetime.utcfromtimestamp(et)


def json2datetime(jt):
    return epoch2datetime(int(jt))


def datetime2json(dt):
    e = datetime2epoch(dt)
    return json.dumps(e)


def is_epoch_legal(et):
    d0 = datetime.now()
    e0 = datetime2epoch(d0)
    latest_month = 2
    el = e0 + latest_month * 31 * 24 * 60 * 60
    if e0 < et < el:
        return True
    return False


def is_slot_legal(t_from_raw, t_to_raw):
    if t_from_raw.isdigit() and t_to_raw.isdigit():
        t_from = int(t_from_raw)
        t_to = int(t_to_raw)
        if t_from % 3600 == 0 and t_to % 3600 == 0:
            if is_epoch_legal(t_from) and is_epoch_legal(t_to) and t_to - t_from >= 3600:
                return True
    return False

