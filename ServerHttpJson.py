
import cherrypy as cp
import json


class Servidor(object):

    @cp.tools.accept(media='application/json')

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def json_in(self):
        print(cp.request.json['filter'])
        return {}

    @cp.expose
    def index(self):
        return "<html><body>Hola Mundo</body></html>!"

    @cp.expose
    def update(self):
        print("entro")
        cl = cp.request.headers['Content-Length']
        #rawbody = cherrypy.request.body.read(int(cl))
        rawData = cp.request.body.read(int(cp.request.headers['Content-Length']))
        b = json.load(rawData)
        #body = json.loads(str(rawbody))
        print(b)
        return "Updated r%." % (b,)


    cp.config.update({'server.socket_host':'0.0.0.0','server.socket_port':9000})

if __name__=='__main__':
    cp.config.update({'server.socket_host':'0.0.0.0','server.socket_port':9000})
    cp.quickstart(Servidor())