from facebookads.adobjects.abstractobject import AbstractObject

class Like(AbstractObject):
    from facebookads.adobjects.page import Page
    class Field(Page.PublicField):
        pass

    @classmethod
    def get_endpoint(cls):
        return 'likes'
