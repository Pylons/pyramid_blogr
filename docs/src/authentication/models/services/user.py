from ..meta import DBSession
from ..user import User

class UserService(object):

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()
