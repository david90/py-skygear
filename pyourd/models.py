class Record:
    def __init__(self, id, owner_id, acl, **kwargs):
        self._id = id
        self._owner_id = owner_id
        self._acl = acl
        self._data = kwargs or {}

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, item):
        return item in self._data

    @property
    def id(self):
        return self._id

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def acl(self):
        return self._acl

    @property
    def data(self):
        return self._data


# RecordID is immutable. Developer is not expected to modify a record's id
# once instantiated
class RecordID:
    def __init__(self, type_, key):
        if not type_:
            raise ValueError('RecordID.type cannot be None or empty')
        if not key:
            raise ValueError('RecordID.key cannot be None or empty')
        self._type = type_
        self._key = key

    @property
    def type(self):
        return self._type

    @property
    def key(self):
        return self._key


ACCESS_CONTROL_ENTRY_LEVEL_WRITE = 'write'
ACCESS_CONTROL_ENTRY_LEVEL_READ = 'read'


class AccessControlEntry:
    def __init__(self, level):
        self.level = level


ACCESS_CONTROL_ENTRY_RELATION_FRIEND = 'friend'
ACCESS_CONTROL_ENTRY_RELATION_FOLLOW = 'follow'


class RelationalAccessControlEntry(AccessControlEntry):
    def __init__(self, relation, level):
        super().__init__(level)
        self.relation = relation


class DirectAccessControlEntry(AccessControlEntry):
    def __init__(self, user_id, level):
        super().__init__(level)
        self.user_id = user_id


class Asset:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError('Asset.name cannot be None or empty')
        self._name = name


class Reference:
    def __init__(self, recordID):
        self.recordID = recordID

    @property
    def recordID(self):
        return self._recordID

    @recordID.setter
    def recordID(self, recordID):
        if recordID is None:
            raise ValueError('Reference.recordID cannot be None')
        self._recordID = recordID
