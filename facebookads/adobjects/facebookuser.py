from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.adobjects.facebookuseraccount import FacebookUserAccount
from facebookads.adobjects.userpermission import UserPermission
from facebookads.adobjects.like import Like
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)


class FacebookUser(AbstractCrudObject, CannotDelete, CannotCreate, CannotUpdate):
    class Field(object):
        id = 'id'
        about = 'about'
        address = 'address'
        age_range = 'age_range'
        bio = 'bio'
        birthday = 'birthday'
        context = 'context'
        currency = 'currency'
        devices = 'devices'
        education = 'education'
        email = 'email'
        favorite_athletes = 'favorite_athletes'
        favorite_teams = 'favorite_teams'
        first_name = 'first_name'
        gender = 'gender'
        hometown = 'hometown'
        inspirational_people = 'inspirational_people'
        install_type = 'install_type'
        installed = 'installed'
        interested_in = 'interested_in'
        is_shared_login = 'is_shared_login'
        is_verified = 'is_verified'
        languages = 'languages'
        last_name = 'last_name'
        link = 'link'
        location = 'location'
        locale = 'locale'
        meeting_for = 'meeting_for'
        middle_name = 'middle_name'
        name = 'name'
        name_format = 'name_format'
        payment_pricepoints = 'payment_pricepoints'
        test_group = 'test_group'
        political = 'political'
        relationship_status = 'relationship_status'
        religion = 'religion'
        security_settings = 'security_settings'
        significant_other = 'significant_other'
        sports = 'sports'
        quotes = 'quotes'
        third_party_id = 'third_party_id'
        timezone = 'timezone'
        token_for_business = 'token_for_business'
        updated_time = 'updated_time'
        shared_login_upgrade_required_by = 'shared_login_upgrade_required_by'
        verified = 'verified'
        video_upload_limits = 'video_upload_limits'
        viewer_can_send_gift = 'viewer_can_send_gift'
        website = 'website'
        work = 'work'
        public_key = 'public_key'
        cover = 'cover'

    def get_friends(self, fields=None, params=None):
        return self.iterate_edge(Friend, fields, params)

    def get_taggable_friends(self, fields=None, params=None):
        return self.iterate_edge(TaggableFriend, fields, params)

    def get_events(self, fields=None, params=None):
        from facebookads.adobjects.event import UserEvents
        return self.iterate_edge(UserEvents, fields, params)

    def get_accounts(self, fields=None, params=None):
        return self.iterate_edge(FacebookUserAccount, fields, params)

    def get_permissions(self, fields=None, params=None):
        return self.iterate_edge(UserPermission, fields, params)

    def get_likes(self, fields=None, params=None):
        return self.iterate_edge(Like, fields, params)

class Friend(AbstractCrudObject, CannotCreate, CannotUpdate, CannotDelete):
    class Field(FacebookUser.Field):
        pass

    @classmethod
    def get_endpoint(cls):
        return 'friends'


class TaggableFriend(AbstractCrudObject, CannotCreate, CannotUpdate, CannotDelete):
    class Field(FacebookUser.Field):
        pass

    @classmethod
    def get_endpoint(cls):
        return 'taggable_friends'
