from facebookads.adobjects.abstractobject import AbstractObject
from facebookads.adobjects.event import Event
from facebookads.api import FacebookRequest
from facebookads.typechecker import TypeChecker
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)


class UserEvents(CannotCreate, CannotDelete, CannotUpdate, AbstractObject):
    class Field(Event.Field):
        rsvp_status = 'rsvp_status'

    @classmethod
    def get_endpoint(cls):
        return 'events'