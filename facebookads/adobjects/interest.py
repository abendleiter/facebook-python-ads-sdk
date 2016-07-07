from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
)

class Interest(CannotCreate, CannotDelete, AbstractCrudObject):
    class Field(object):
        id = 'id'
        audience_size = 'audience_size'
        name = 'name'
