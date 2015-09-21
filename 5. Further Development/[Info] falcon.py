# things.py
# Let's get this party started
import falcon
import json
# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        param = req._params
        resp.status = falcon.HTTP_200  # This is the default status
        func = param.pop('func','')
        result = getattr(self, func)(**param)
        resp.body = json.dumps(result)
    def add(self,a,b):
        return {'data':int(a)+int(b)}
    def minus(self,a,b):
        return {'data':int(a)-int(b)}
    def mult(self,a,b):
        return {'data':int(a)*int(b)}
    def gender(self,user_id):
        return {'data':{'male':70,'female':80}}
# falcon.API instances are callable WSGI apps
app = falcon.API()
# Resources are represented by long-lived class instances
things = ThingsResource()
# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
