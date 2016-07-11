from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
)
from facebookads.adobjects.page import Page, UserPagePermission

class BusinessManager(CannotCreate, CannotDelete, AbstractCrudObject):
    class Field(object):
        id = 'id'
        name = 'name'
        native_app_store_ids = 'native_app_store_ids'
        native_app_targeting_ids = 'native_app_targeting_ids'
        og_actions = 'og_actions'
        og_namespace = 'og_namespace'
        og_objects = 'og_objects'
        picture = 'picture'
        supported_platforms = 'supported_platforms'
        tabs = 'tabs'
        type = 'type'
        url = 'url'
        page_permissions = 'page_permissions'

    @classmethod
    def get_endpoint(cls):
        return ''

    @classmethod
    def get_default_read_fields(cls):
        return [cls.Field.id, cls.Field.name]

    def get_pages(self, fields=None, params=None):
        return self.iterate_edge(Page, fields, params)

    def get_user_permissions(self, fields=None, params=None):
        return self.iterate_edge(UserPagePermission, fields, params)
