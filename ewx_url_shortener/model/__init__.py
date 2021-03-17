

class StorageBase:
    """
    Storage abstraction class
    This abstract class should be implemented by the wrapper class of choice
    this wrapper class should implement all the abstract methods of this class

    A good idea is to implement a redis wrapper for testing
    """

    def url_already_exists(self, url):
        raise NotImplementedError

    def store_url(self, url, short_code):
        raise NotImplementedError

    def update_url_stats(self, url):
        raise NotImplementedError

    def short_code_exists(self, short_code):
        raise NotImplementedError

    def get_short_code_by_url(self, url):
        raise NotImplementedError

    def get_short_code_info_by_url(self, url):
        raise NotImplementedError


