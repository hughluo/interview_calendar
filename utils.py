import json
from datetime import datetime
import time
# bunch of utilities functions


def log(*args, **kwargs):
    """
    Using log to replace print for better debugging.
    All logs will be saved in calendar.log.txt
    """
    t_format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(t_format, value)
    with open('calendar.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


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
    latest_month = 2  # set the latest valid slot input here
    el = e0 + latest_month * 31 * 24 * 60 * 60
    if e0 < et < el:
        return True
    return False


def is_slot_legal(t_from_raw, t_to_raw):
    if t_from_raw.isdigit() and t_to_raw.isdigit():
        t_from = int(t_from_raw)
        t_to = int(t_to_raw)
        if t_from % 3600 == 0 and t_to % 3600 == 0:  # slot should be sharp (o'clock)
            if is_epoch_legal(t_from) and is_epoch_legal(t_to):
                if t_to - t_from >= 3600:  # slot period should no less than one hour
                    return True
    return False


def pprint_matching(ms):
    """
    Pretty print for matching result.
    For debugging purpose.
    """
    for m in ms:
        print('From {} to {}, Candidate id: {}, Interviewer id: {}'.format(
                epoch2datetime(m['t_start']),
                epoch2datetime(m['t_end']),
                m['cid'], m['iids']
            )
        )
