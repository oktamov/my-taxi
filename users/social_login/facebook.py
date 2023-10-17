import facebook


class Facebook:  # noqa
    """
    Facebook class to fetch the user info and return it
    """

    @staticmethod
    def validate(auth_token):
        """
        Validate method Queries the facebook GraphAPI to fetch the user info
        """
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request("/me?fields=name,email")
            return profile  # noqa
        except:  # noqa
            return "The token is invalid or expired."
