from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)

class FacebookUserAccount(AbstractCrudObject, CannotCreate, CannotDelete, CannotUpdate):

    class Field:
        id = 'id'
        name = 'name'
        category = 'category'
        perms = 'perms'

    @classmethod
    def get_endpoint(cls):
        return 'accounts'

