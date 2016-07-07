from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)

class UserPermission(AbstractCrudObject, CannotCreate, CannotDelete, CannotUpdate):

    class Field:
        id = 'id'
        permission = 'permission'
        status = 'status'

    @classmethod
    def get_endpoint(cls):
        return 'permissions'

    def get_id(self):
        return None

    def get_id_assured(self):
        return None
