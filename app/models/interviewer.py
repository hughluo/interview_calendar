from app.models import Model


class Interviewer(Model):
    __fields__ = Model.__fields__ + [
        ('name', str, ''),
        ('slots', list, []),
    ]

    @classmethod
    def add_slot_by_id(cls, iid, t_from, t_to):
        """
        Add an available interview time slot

        Schema: one to few, therefore, embed the slots in Interviewer Document.

        :param t_from: time from
        :param t_to: time to
        :return: if success return the presentation of Interviewer obj
        """

        ss = cls.get_slots_by_id(iid)
        s = {
            't_from': t_from,
            't_to': t_to,
        }
        ss.append(s)
        cls.find_by_id_and_update(iid, slots=ss)

    @classmethod
    def get_slots_by_id(cls, iid):
        c = cls.find_one(id=iid)
        ss = c.slots
        return ss

    @classmethod
    def del_all_slots_by_id(cls, iid):
        ss = []
        cls.find_by_id_and_update(iid, slots=ss)




