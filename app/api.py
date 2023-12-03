import urllib.request
import base64
import json
import os
import ssl

class UrlCall:
    def __init__(self,headers) -> None:
        self.headers=headers

    def allowSelfSignedHttps(self,allowed):
        """ allow to connect azure using env variable """
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context


    def url_call(self,data,url):
        body = str.encode(json.dumps(data))
        req = urllib.request.Request(url,body, self.headers)
        try:  
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            prediction=int(result["Results"][0])
            return prediction

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))
        
