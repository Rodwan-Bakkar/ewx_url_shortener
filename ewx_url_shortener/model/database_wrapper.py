

class DatabaseWrapper:
    DATABASE = {}

    def __init__(self):
        pass

    def url_already_exists(self, url):
        if url in list(self.DATABASE.keys()):
            return True
        return False

    def store_url(self, url, short_code):
        self.DATABASE[url] = short_code

    def short_code_exists(self, short_code):
        if short_code in list(self.DATABASE.values()):
            return True
        return False

