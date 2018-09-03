from app.models import Model
from . interviewer import Interviewer


class Candidate(Model):
    __fields__ = Model.__fields__ + [
        ('name', str, ''),
        ('slots', list, []),
    ]

    @classmethod
    def add_slot_by_id(cls, cid, t_from, t_to):
        """
        Add an available interview time slot

        Schema: one to few, therefore, embed the slots in Candidate Document.

        :param t_from: time from
        :param t_to: time to
        :return: if success return the presentation of Interviewer obj
        """

        ss = cls.get_slots_by_id(cid)
        s = {
            't_from': t_from,
            't_to': t_to,
             }
        ss.append(s)
        cls.find_by_id_and_update(cid, slots=ss)

    @classmethod
    def get_slots_by_id(cls, cid):
        c = cls.find_one(id=cid)
        ss = c.slots
        return ss

    @classmethod
    def get_matching_by_id(cls, cid, iids):
        ms = []
        c_ss = cls.get_slots_by_id(cid)
        for c_s in c_ss:
            ct = int(c_s.get('t_to', -1))
            cf = int(c_s.get('t_from', -1))
            p = ct - cf
            ns = p // 3600  # how many hours with a candidates slot

            for i in range(ns):
                s_s = cf + i * 3600  # start time of a interview slot
                s_e = cf + (i + 1) * 3600  # end time of a interview slot
                ivs = []  # storage iid of interviewers who are available in given interview slot

                for iid in iids:
                    i_ss = Interviewer.get_slots_by_id(iid)

                    for i_s in i_ss:
                        ivt = i_s.get('t_to', -1)
                        ivf = i_s.get('t_from', -1)
                        if ivf <= s_s and ivt >= s_e:
                            ivs.append(iid)

                if len(ivs) > 0:  # which means we have at least one interviewer who is available
                    m = {
                        't_start': s_s,
                        't_end': s_e,
                        'cid': cid,
                        'iids': ivs,
                    }
                    ms.append(m)
        return ms

    @classmethod
    def del_all_slots_by_id(cls, cid):
        ss = []
        cls.find_by_id_and_update(cid, slots=ss)



    # @classmethod
    # def get_matching_by_id_old(cls, cid, iids):
    #     ms = []
    #     c_slots = cls.get_slots_by_id(cid)
    #     for c_s in c_slots:
    #         cf = c_s.t_from
    #         ct = c_s.t_to
    #         for iid in iids:
    #             i_slots = Interviewer.get_slots_by_id(iid)
    #             for i_s in i_slots:
    #                 ivf = i_s.t_from
    #                 ivt = i_s.t_to
    #                 if max(cf, ivf) - min(ct, ivt) >= 3600:
    #                     m = {
    #                         't_from': max(cf, ivf),
    #                         't_to': min(ct, ivt),
    #                         'interviewer': iid,
    #                          }
    #                     ms.append(m)




    # @classmethod
    # def auto_match_by_id(cls, id):
    #     """
    #     Return a list of interviewers who match the slots of given candidate
    #     """
    #     ms = []
    #     c_slots = cls.get_slots_by_id(id)
    #     ivs = Interviewer.all()
    #     for s in c_slots:
    #         cf = s.t_from
    #         ct = s.t_to
    #         for iv in ivs:
    #             for s in iv.slots:
    #                 ivf = s.t_from
    #                 ivt = s.t_to
    #                 # if they have shared time period bigger than 3600 seconds, it's a matching
    #                 if max(cf, ivf) - min(ct, ivt) >= 3600:
    #                     m = {
    #                         't_from': max(cf, ivf),
    #                         't_to': min(ct, ivt),
    #                         'interviewer': iv.id,
    #                     }
    #                     ms.append(m)
    #     for m in ms:
    #         # TODO matching interviewer with each other here...
    #         pass

    @classmethod
    def find_by_name(cls, name):
        """
        Return a Candidate obj by name filtering

        :param name: name of candidate
        :return: Candidate obj
        """
        pass




