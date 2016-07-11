from facebookads.adobjects.abstractobject import AbstractObject
from facebookads.adobjects.abstractcrudobject import AbstractCrudObject
from facebookads.api import FacebookRequest
from facebookads.adobjects.objectparser import ObjectParser
from facebookads.mixins import (
    CannotCreate,
    CannotDelete,
    CannotUpdate,
)


class OAuthAccessTokenResponse(CannotCreate, CannotUpdate, CannotDelete, AbstractCrudObject):
    pass


class OAuthAccessToken(CannotCreate, CannotUpdate, CannotDelete, AbstractCrudObject):

    class GrantType(object):
        fb_exchange_token = 'fb_exchange_token'


    class Field(object):
        id = 'id'
        grant_type = 'grant_type'
        client_id = 'client_id'
        client_secret = 'client_secret'
        fb_exchange_token = 'fb_exchange_token'
        redirect_uri = 'redirect_uri'

    def extend_token(
        self,
        redirect_uri,
        client_id,
        client_secret,
        fb_exchange_token,
        grant_type,
    ):
        request = FacebookRequest(
            node_id='oauth',
            method='GET',
            endpoint='access_token',
            api=self._api,
            target_class=OAuthAccessTokenResponse,
            response_parser=ObjectParser(target_class=OAuthAccessTokenResponse),
        )
        request.add_params({
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'fb_exchange_token': fb_exchange_token,
            'grant_type': grant_type,
        })
        return request.execute()