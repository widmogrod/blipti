import urllib, urllib2;

USER_AGENT = "blipapi - Blip.pl api library for python"
API_VERSION = 0.02
URL = 'http://api.blip.pl'


class Request(object):
    """
    Request object dla api.blip.pl
    """
    def __init__(self, credentials, url, method, data, content_type = None):
        """
        credentials = (username, password)
        url = update_url
        method = POST || GET
        data = string with POST data or dict to encode
        content_type = HTTP header with content type (multipart/form-data)
        """

        self.credentials = credentials
        self.url = '%s%s' % (URL, url)
        self.method = method
        self.data = None

        if type(data) == dict:
            for key, val in data.iteritems():
                if isinstance(val, unicode):
                    data[key] = val.encode('utf-8')
                else:
                    data[key] = val
            self.data = urllib.urlencode(data)

        self.content_type = content_type or  'application/x-www-form-urlencoded'

    def do_request(self):
        request = urllib2.Request(self.url)

        if self.credentials:
            request.add_header('Authorization', 'Basic %s' % (base64.b64encode('%s:%s' % self.credentials)))

        request.add_header('User-Agent', USER_AGENT)
        request.add_header('X-blip-api', '%s' % API_VERSION)
        request.add_header('Accept', 'application/json')
        request.add_header('Pragma', 'no-cache')

        if self.data:
            request.add_data(self.data)
            request.add_header('Content-Type', self.content_type )
            request.add_header('Content-Length', len(self.data))

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            # 201 - Created:
            data = e.read()
            if e.code == 201:
                return True
            #raise e
            return data
        data = response.read()
        return data


class Account(object):
    def __init__(self, username= None, password = None):
        self.credentials = None
        if username is not None and password is not None:
            self.set_credentials(username, password)

    def set_credentials(self, username, password):
        self.credentials = (username, password)



class BlipAPI:
    def __init__(self, credentials = None):
        self.set_credentials(credentials);

    def set_credentials(self, credentials):
        """
        Ustaw uprawnienia
        """

        if credentials is Account:
            self.credentials = credentials;

    def clear_credentials(self):
        """
        Wyczysc uprawnienia
        """

        self.credentials = None

    def get_all_statuses(self, limit = None):
        """
        Pobiera ostatnie statusy
        """

        url = "/statuses/all"

        if limit is int:
             url = "%s?limit=%d" % (url, limit)

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_user_statuses(self, user, limit = None):
        """
        Pobiera statusy uzytkownika
        """

        if type(user) != str:
            return False

        url = "/users/%s/statuses" % user

        if type(limit) == int:
             url = "%s?limit=%d" % (url, limit)
        
        request = Request(None, url, "GET", None);
        return request.do_request();

    def get_tags(self, tag, limit = None):
        """
        Zwraca do 'limit' najnowszych statusow otagowanych 'tag' ..
        """

        if type(tag) != str:
            return False

        url = "/tags/%s" % tag

        if type(limit) == int:
            url = "%s?limit=%d" % (url, limit)

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_tags_since(self, tag, since = None):
        """
        Zwraca do 'limit' najnowszych statusow otagowanych 'tag' ..
        """

        if type(tag) != str:
            return False

        url = "/tags/%s" % tag

        if type(since) == int:
            url = "%s/since/%d" % (url, since)

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_all_pictures(self, limit = None):
        """
        Zwraca 'limit' najnowszych obrazkow od wszystkich uzytkownikow 
        """

        url = "/pictures/all"

        if limit is int:
             url = "%s?limit=%d" % (url, limit)

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_all_shortlinks(self, limit = None):
        """
        Zwraca 'limit' najnowszych linkow (rdir.pl) od wszystkich uzytkownikow 
        """

        url = "/shortlinks/all"

        if limit is int:
             url = "%s?limit=%d" % (url, limit)

        request = Request(None, url, "GET", None);
        return request.do_request();

    def get_all_bliposphere(self):
        """
        Zwraca obecna zawartosc bliposfery 
        """

        url = "/bliposphere"

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_user(self, user):
        """
        Zwraca uzytkownika 'user'
        """

        if type(user) != str:
            return False

        url = "/users/%s" % user

        request = Request(None, url, "GET", None);
        return request.do_request();
    
    def get_avatar(self, user):
        """
        Zwraca awatar uzytkownika 'user'
        """

        if type(user) != str:
            return False

        url = "/users/%s/avatar" % user

        request = Request(None, url, "GET", None);
        return request.do_request();
