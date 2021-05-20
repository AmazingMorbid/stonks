
class Unauthorized(Exception):
    def __init__(self):
        super(Unauthorized, self).__init__("Unauthorized.")


class MissingGrantType(Exception):
    def __init__(self):
        super(MissingGrantType, self).__init__("Missing grant type.")


class CouldNotAuthorize(Exception):
    def __init__(self):
        super(CouldNotAuthorize, self).__init__("allegro-sdk tried to authenticate but failed. Check your "
                                                "credentials.")
