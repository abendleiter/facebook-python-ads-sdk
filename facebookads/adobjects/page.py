# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from facebookads.adobjects.leadgenform import LeadgenForm
from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.adobjects.objectparser import ObjectParser
from facebookads.api import FacebookRequest
from facebookads.typechecker import TypeChecker
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)

class UserPagePermission(AbstractCrudObject):
    class Field(object):
        role = 'role'
        business = 'business'
        user = 'user'
        id = 'id'

    @classmethod
    def get_endpoint(cls):
        return 'userpermissions'

    def get_node_path(self):
        return (self.get_parent_id_assured(), self.get_endpoint())


class PageEvents(AbstractCrudObject):
    @classmethod
    def get_endpoint(cls):
        return 'events'


class Page(CannotCreate, CannotDelete, CannotUpdate, AbstractCrudObject):
    class CommonField(object):
        category = 'category'
        id = 'id'
        name = 'name'

    class PublicOnlyField(object):
        # public fields
        about = 'about'
        category = 'category'
        checkins = 'checkins'
        country_page_likes = 'country_page_likes'
        cover = 'cover'
        description = 'description'
        emails = 'emails'
        has_added_app = 'has_added_app'
        is_community_page = 'is_community_page'
        is_published = 'is_published'
        likes = 'likes'
        link = 'link'
        location = 'location'
        new_like_count = 'new_like_count'
        phone = 'phone'
        talking_about_count = 'talking_about_count'
        username = 'username'
        website = 'website'
        were_here_count = 'were_here_count'

    class AdminOnlyField(object):
        access_status = 'access_status'
        access_type = 'access_type'
        category_list = 'category_list'
        permitted_roles = 'permitted_roles'

    class PublicField(CommonField, PublicOnlyField):
        pass

    class AdminField(CommonField, AdminOnlyField):
        class PermittedRoles(object):
            advertiser = 'ADVERTISER'
            content_creator = 'CONTENT_CREATOR'
            insights_analyst = 'INSIGHTS_ANALYST'
            manager = 'MANAGER'
            moderator = 'MODERATOR'

    class Field(PublicField, AdminField):
        pass

    class Location(object):
        city = 'city'
        country = 'country'
        latitude = 'latitude'
        longitude = 'longitude'
        street = 'street'
        zip = 'zip'

    @classmethod
    def get_endpoint(cls):
        return 'pages'

    def get_leadgen_forms(self, fields=None, params=None):
        """
        Returns all leadgen forms on the page
        """
        return self.iterate_edge(LeadgenForm, fields, params, endpoint='leadgen_forms')

    def get_likes(self, fields=None, params=None):
        return self.iterate_edge(Like, fields, params)

    def get_events(self, fields=None, params=None):
        return self.iterate_edge(PageEvents, fields, params)

    def get_user_permissions(self, fields=None, params=None):
        return self.iterate_edge(UserPagePermission, fields, params)

    def add_user_permission(self, user_id, business_id, role):
        permission = UserPagePermission(parent_id=self.get_id_assured(), api=self.get_api())
        permission.remote_create(params={'user': user_id, 'business': business_id, 'role': role})

    def remove_user_permission(self, user_id, business_id):
        request = FacebookRequest(
            node_id=self.get_id_assured(),
            method='DELETE',
            endpoint=UserPagePermission.get_endpoint(),
            api=self.get_api(),
        )
        request.add_params({'user': user_id, 'business': business_id})
        request.execute()
