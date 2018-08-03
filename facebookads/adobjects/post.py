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

from facebookads.adobjects.abstractobject import AbstractObject
from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.adobjects.objectparser import ObjectParser
from facebookads.adobjects.facebookuser import FacebookUser
from facebookads.api import FacebookRequest
from facebookads.typechecker import TypeChecker
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)

from facebookads.api import FacebookRequest
from facebookads.typechecker import TypeChecker

"""
This class is auto-generated.

For any issues or feature requests related to this class, please let us know on
github and we'll fix in our codegen framework. We'll not be able to accept
pull request for this class.
"""

class Post(
    AbstractCrudObject,
):

    def __init__(self, fbid=None, parent_id=None, api=None):
        self._isPost = True
        super(Post, self).__init__(fbid, parent_id, api)

    class Field(AbstractObject.Field):
        message = 'message'
        created_time = 'created_time'
        is_published = 'is_published'
        description = 'description'
        message_tags = 'message_tags'
        likes = 'likes.summary(true)'
        shares = 'shares.summary(true)'
        reactions = 'reactions.summary(true)'
        link = 'link'
        permalink_url = 'permalink_url'
        type = 'type'
        status_type = 'status_type'
        place = 'place'
        shares = 'shares'
        full_picture = 'full_picture'
        picture = 'picture'
        name = 'name'
        promotable_id = 'promotable_id'
        from_user = 'from'
        id = 'id'

    class StatusType:
        mobile_status_update = 'mobile_status_update'
        created_note = 'created_note'
        added_photos = 'added_photos'
        added_video = 'added_video'
        shared_story = 'shared_story'
        created_group = 'created_group'
        created_event = 'created_event'
        wall_post = 'wall_post'
        app_created_story = 'app_created_story'
        published_story = 'published_story'
        tagged_in_photo = 'tagged_in_photo'
        approved_friend = 'approved_friend'

    _field_types = {
        'message': 'string',
        'created_time': 'datetime',
        'is_published' : 'bool',
        'likes': 'Object',
        'shares': 'Object',
        'reactions': 'Object',
        'description' : 'string',
        'message_tags' : 'Object',
        'link' : 'string',
        'permalink_url' : 'string',
        'type' : 'string',
        'status_type' : 'string',
        'place' : 'Object',
        'shares' : 'Object',
        'full_picture' : 'string',
        'picture' : 'string',
        'name' : 'string',
        'id' : 'string',
        'from': 'Object',
        'promotable_id': 'string'
    }

    class Type:
        link = 'link'
        status = 'status'
        photo = 'photo'
        video = 'video'
        offer = 'offer'

    def api_get(self, fields=None, params=None, batch=None, pending=False):
        param_types = {
        }
        enums = {
        }
        request = FacebookRequest(
            node_id=self['id'],
            method='GET',
            endpoint='/',
            api=self._api,
            param_checker=TypeChecker(param_types, enums),
            target_class=Post,
            api_type='NODE',
            response_parser=ObjectParser(reuse_object=self),
        )
        request.add_params(params)
        request.add_fields(fields)

        if batch is not None:
            request.add_to_batch(batch)
            return request
        elif pending:
            return request
        else:
            self.assure_call()
            return request.execute()


    @classmethod
    def _get_field_enum_info(cls):
        field_enum_info = {}
        field_enum_info['StatusType'] = Post.StatusType.__dict__.values()
        field_enum_info['Type'] = Post.Type.__dict__.values()
        return field_enum_info
