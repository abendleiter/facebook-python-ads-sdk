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

"""
The exceptions module contains Exception subclasses whose instances might be
raised by the sdk.
"""

import json
import re
import collections.abc


class FacebookError(Exception):
    """
    All errors specific to Facebook api requests and Facebook ads design will be
    subclassed from FacebookError which is subclassed from Exception.
    """
    pass


class FacebookRequestError(FacebookError):
    """
    Raised when an api request fails. Returned by error() method on a
    FacebookResponse object returned through a callback function (relevant
    only for failure callbacks) if not raised at the core api call method.
    """

    def __init__(
        self, message,
        request_context,
        http_status,
        http_headers,
        body
    ):
        self._message = message
        self._request_context = request_context
        self._http_status = http_status
        self._http_headers = http_headers
        try:
            self._body = json.loads(body)
        except (TypeError, ValueError):
            self._body = body

        self._api_error_code = None
        self._api_error_subcode = None
        self._api_error_type = None
        self._api_error_message = None
        self._api_error_subcode = None
        self._api_blame_field_specs = None
        self._api_transient_error = False

        if self._body and isinstance(self._body, dict) and 'error' in self._body:
            self._error = self._body['error']
            if 'message' in self._error:
                self._api_error_message = self._error['message']
            if 'code' in self._error:
                self._api_error_code = self._error['code']
            if 'is_transient' in self._error:
                self._api_transient_error = self._error['is_transient']
            if 'error_subcode' in self._error:
                self._api_error_subcode = self._error['error_subcode']
            if 'type' in self._error:
                self._api_error_type = self._error['type']
            # workaround for malformed error responses:
            error_data = self._error.get('error_data', {})
            if type(error_data) == dict and error_data.get('blame_field_specs'):
                self._api_blame_field_specs = \
                    self._error['error_data']['blame_field_specs']
        else:
            self._error = None

        # We do not want to print the file bytes
        request = self._request_context
        if 'files' in self._request_context:
            request = self._request_context.copy()
            del request['files']

        super(FacebookRequestError, self).__init__(
            "\n\n" +
            "  Message: %s\n" % self._message +
            "  Method:  %s\n" % request.get('method') +
            "  Path:    %s\n" % request.get('path', '/') +
            "  Params:  %s\n" % request.get('params') +
            "\n" +
            "  Status:  %s\n" % self._http_status +
            "  Response:\n    %s" % re.sub(
                r"\n", "\n    ",
                json.dumps(self._body, indent=2)
            ) +
            "\n"
        )

    def request_context(self):
        return self._request_context

    def http_status(self):
        return self._http_status

    def http_headers(self):
        return self._http_headers

    def body(self):
        return self._body

    def api_error_message(self):
        return self._api_error_message

    def api_error_code(self):
        return self._api_error_code

    def api_error_subcode(self):
        return self._api_error_subcode

    def api_error_type(self):
        return self._api_error_type

    def api_blame_field_specs(self):
        return self._api_blame_field_specs

    def api_transient_error(self):
        return self._api_transient_error

    def get_message(self):
        return self._message

    @property
    def _sentry_data(self):
        # AB-477 Make FacebookRequestErrors easier to tell apart
        tags = {}
        extra = {}

        headers = self.http_headers()
        wanted = ('X-FB-Debug', 'X-FB-Rev', 'X-FB-Trace-ID')
        if headers:
            for name in (n for n in headers if n in wanted):
                extra[name] = headers[name]

        errdata = (
            ('FB-error-type', self.api_error_type()),
            ('FB-error-code', self.api_error_code()),
            ('FB-error-subcode', self.api_error_subcode()),
            ('FB-error-message', self.api_error_message()),
        )
        errtags = {'FB-error-type'}
        for key, value in errdata:
            extra[key] = str(value)
            if key in errtags:
                tags[key] = value

        return dict(tags=tags, extra=extra)

    @classmethod
    def from_exception(cls, e):
        """
        helper method to instantiate inherited class of FacebookRequestError

        Args:
            e: the original FacebookRequestError

        Returns: an instance of this class, populated with the FacebookRequestError data
        """
        return cls(
            message=e._message,
            request_context=e._request_context,
            http_status=e._http_status,
            http_headers=e._http_headers,
            body=e._body,
        )


class FacebookBadResponseError(FacebookRequestError):
    """ A Facebook API response is not parseable as a JSON dict.

        It might be an HTML error page instead, and possibly still have a
        status of 200.
    """
    @classmethod
    def check_bad_response(cls, facebook_response):
        # AB-477: response body is not a JSON object (but possibly an HTML error page)
        # AB-1107: generalized FacebookBadResponseError for AbstractCrudObject.remote_read
        if not isinstance(facebook_response.json(), collections.abc.MutableMapping):
            raise FacebookBadResponseError(
                "API call did not return a JSON object",
                facebook_response._call,
                facebook_response.status(),
                facebook_response.headers(),
                facebook_response.body()
            )


class FacebookRequestSubError(FacebookRequestError):
    """ Base class for more specific facebook reqeust errors """
    ERROR_CODES = None  # list of (errorcode, subcode). The subcode can also be `all` as a wildcard

    @classmethod
    def can_catch(cls, exception):
        error_code, error_sub_code = (exception.api_error_code(), exception.api_error_subcode())
        return (
            (error_code, error_sub_code) in cls.ERROR_CODES
            or
            (error_code, all) in cls.ERROR_CODES  # wildcard error codes
        )


class FacebookTransientError(FacebookRequestSubError):

    # "error_user_title": "Try Again Soon",
    # "message": "Service temporarily unavailable",
    # "error_user_msg": "Sorry, there's a temporary problem with this post. Please try again in a few moments.",
    SUBCODE_TRY_AGAIN_SOON = 1342001
    ERROR_CODES = [
        (2, SUBCODE_TRY_AGAIN_SOON),
    ]

    @classmethod
    def can_catch(cls, exception):
        # General Transient Error
        is_transient = False
        body = exception.body()
        if body and type(body) == dict:
            error = body.get('error', False)
            if error and type(error) == dict:
                is_transient = error.get('is_transient', False)
        return is_transient or super().can_catch(exception)


class FacebookAccessTokenInvalid(FacebookRequestSubError):
    """ The Facebook request faile due to an invalid or expired access token. """

    TOKEN_INVALID_CODE = 190  # general error code for token related errors
    SUBCODE_MALFORMED_TOKEN = None
    SUBCODE_INVALID_TOKEN = 467  # invalid access token

    ERROR_CODES = [
        (TOKEN_INVALID_CODE, SUBCODE_INVALID_TOKEN),
        (TOKEN_INVALID_CODE, SUBCODE_MALFORMED_TOKEN),
    ]


class FacebookAccessTokenInvalidUserCheckpointed(FacebookAccessTokenInvalid):
    SUBCODE_USER_CHECKPOINTED = 459  # user needs to login at Facebook to fix this issue
    SUBCODE_USER_IN_BLOCKED_LOGGED_IN_CHECKPOINT = 490  # user is enrolled in a blocking checkpoint
    ERROR_CODES = [
        (FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_USER_CHECKPOINTED),
        (FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_USER_IN_BLOCKED_LOGGED_IN_CHECKPOINT),
    ]


class FacebookAccessTokenInvalidNoAppPermission(FacebookAccessTokenInvalid):
    SUBCODE_NO_APP_PERMISSION = 458  # user did not grand permission for this app
    ERROR_CODES = [(FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_NO_APP_PERMISSION)]


class FacebookAccessTokenInvalidTokenExpired(FacebookAccessTokenInvalid):
    SUBCODE_TOKEN_EXPIRED = 463  # user access token expired
    ERROR_CODES = [(FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_TOKEN_EXPIRED)]


class FacebookAccessTokenInvalidUnconfirmedUser(FacebookAccessTokenInvalid):
    SUBCODE_UNCONFIRMED_USER = 464  # user is not a confirmed user
    ERROR_CODES = [(FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_UNCONFIRMED_USER)]


class FacebookAccessTokenInvalidSessionInvalid(FacebookAccessTokenInvalid):
    SUBCODE_SESSION_INVALID = 461  # invalid session
    ERROR_CODES = [(FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_SESSION_INVALID)]


class FacebookAccessTokenInvalidPasswordChanged(FacebookAccessTokenInvalid):
    SUBCODE_PASSWORD_CHANGED = 460  # user changed password, so the token is no longer valid
    ERROR_CODES = [(FacebookAccessTokenInvalid.TOKEN_INVALID_CODE, SUBCODE_PASSWORD_CHANGED)]


class FacebookBadObjectError(FacebookError):
    """Raised when a guarantee about the object validity fails."""
    pass


class FacebookBadParameterError(FacebookError):
    """Raised when a guarantee about the parameter validity fails."""
    pass


class FacebookUnavailablePropertyException(FacebookError):
    """Raised when an object's property or method is not available."""
    pass


class FacebookCantEditAdsetException(FacebookRequestSubError):
    """
     Response: { "error": {
     "code": 100,
     "type": "OAuthException",
     "is_transient": false,
     "error_subcode": 1487056,
     "message": "Invalid parameter",
     "error_user_title":
     "Can't Edit Ad Set",
     "error_user_msg": "You can't edit this ad set. You can only edit active or paused ad sets." }
     }
    """
    ERROR_CODES = [(100, 1487056)]


class FacebookInsufficientPermissionsForAdCreation(FacebookRequestSubError):
    """
    Occurs when an AdCreative should be created, but the we don't have the permissions required
    to create Ads for a particular page.

    Response:
      {
        "error": {
          "message": "Invalid parameter",
          "error_subcode": 1487202,
          "error_user_title": "Only Admins Can Run Ads for Pages",
          "type": "OAuthException",
          "is_transient": false,
          "fbtrace_id": "BHp0+PsitNI",
          "code": 100,
          "error_user_msg": "If you want to create an ad, please ask the Facebook Page manager to
          give you permission by adding you to admin, editor or advertiser page roles."
        }
      }
    """
    ERROR_CODES = [(100, 1487202)]


class FacebookOopsException(FacebookRequestSubError):
    '''
    Inexplicable errors that almost never occur, but are not very spcific in their existance

    Response:
    {
      "error": {
        "message": "Invalid parameter",
        "error_subcode": 1487390,
        "error_user_title": "Adcreative Create Failed",
        "type": "OAuthException",
        "is_transient": false,
        "fbtrace_id": "APpX9NB5Y0e",
        "code": 100,
        "error_user_msg": "The Adcreative Create Failed for the following reason: Oops, something went wrong. Please try again later"
      }
    }
    '''
    ERROR_CODES = [
        (100, 1487390),
        (2615, all),  #"(#2615) Oops, something went wrong. Please try again later",
    ]


class FacebookUnknownError(FacebookRequestSubError):
    @classmethod
    def can_catch(cls, exception):
        error_message = exception.api_error_message()
        return (
            exception.api_error_code() == 1
            and
            (
                error_message == 'An unknown error occurred'
                or
                error_message == 'An unknown error has occurred.'
            )
        )

class DocsmithSkipTestError(Exception):
    """Raised when a docsmith test is skipped."""
    def __init__(self, message):
        self._message = message

    def get_skip_error_msg(self):
        return self._message


class FacebookBadParameterTypeException(FacebookError):
    """Raised when a parameter or field is set with improper type."""
    pass
