
import cherrypy as cp
import json


class Servidor(object):

    @cp.tools.accept(media='application/json')

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out()
    def json_in(self):
        print(cp.request.json['measurement'])
        return {}

    @cp.expose
    @cp.tools.json_in()
    @cp.tools.json_out(content_type='application/json')
    def measurement(self):
        print(cp.request.json["measurement"])
        js = json.loads(str(cp.request.json["measurement"]).replace("'",'"'))
        print(js["initial_date"])
        return {'key': 'value'}

    @cp.expose
    def index(self):
        return "<html><body>Hola Mundo</body></html>!"

    #def Metodo(self):
        #Ejecutar metodo


if __name__=='__main__':
    #cp.config.update({'server.socket_host':'0.0.0.0','server.socket_port':73 99})
    cp.quickstart(Servidor())