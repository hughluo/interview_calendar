import time
from pymongo import MongoClient
client = MongoClient()
db = client.calender


def get_next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    ds = db['data_id']
    # find_and_modify provided by pymongo is a atomic function
    next_id = ds.find_and_modify(**kwargs).get('seq')
    return next_id


class Model(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def new(cls, form=None, **kwargs):
        # cname stands for collection name
        cname = cls.__name__
        m = cls()
        fields = cls.__fields__.copy()
        # auto-incremented id
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # set default value
                setattr(m, k, v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        m.id = get_next_id(cname)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        # m.deleted = False
        m.type = cname.lower()
        # customize for special model
        # m._setup(form)
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        Retrieve a model from mongodb
        """
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # set default value
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m

    def save(self):
        cname = self.__class__.__name__
        db[cname].save(self.__dict__)

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        """
        use pymongo to query
        """
        name = cls.__name__
        # TODO filter d that marked as deleted
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        dl = [cls._new_with_bson(d) for d in ds]
        return dl

    @classmethod
    def find_one(cls, **kwargs):
        # kwargs['deleted'] = False
        dl = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        if len(dl) > 0:
            return dl[0]
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        d = cls.find_one(id=id)
        return d

    @classmethod
    def check_existence_by_id(cls, id):
        if cls.find_by_id(id) is None:
            return False
        return True

    @classmethod
    def check_all_existence_by_id(cls, ids):
        for id in ids:
            if not cls.check_existence_by_id(id):
                return False
        return True

    @classmethod
    def find_by_id_and_update(cls, id, **kwargs):
        cname = cls.__name__
        return db[cname].find_one_and_update({'id': id}, {'$set': kwargs})




