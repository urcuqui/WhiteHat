import pyshark
import pyshark.packet.packet
import os
import datetime
import traceback

"""Autor: Andrés Pérez
   Proyecto de grado: Sistema de análisis de tráfico de red para la detección de malware en dispositivos Android
   Universidad Icesi, 2018"""

"""Basado en el proyecto de grado: Sistema open source para la deteccion de ataques en paginas web maliciosas, realizado por Melisa Garcia P. y Jose Luis Osorio Q., universidad Icesi, 2017"""
#cap = pyshark.FileCapture('4de0d8997949265a4b5647bb9f9d42926bd88191.pcap')


#Dirección ip del emulador
IP_RED="192.168.131.38"
	

counter=0	
counter2=0


def pkt_without_dns(captura): #N0
    """ Almacena en un arreglo todo los paquetes que no son DNS"""
    print "--------------- Obteniendo pkt sin dns -------------------"
    pkts_temp = []
    pkts_dns = []
    for pkt in captura:
        try:
            if pkt.ip.src == IP_RED:
                for lyr in pkt.layers:
                    if lyr.layer_name in 'dns':
                        if pkt not in pkts_dns:
                            pkts_dns.append(pkt)
                if pkt not in pkts_dns and pkt not in pkts_temp:
                    pkts_temp.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print 'Error en pkt_without_dns'
    return pkts_temp


def tcp_conversation_exchange(captura):  # N1
    """ cuenta la cantidad de paquetes que hay para el protocolo asignado """
    print "--------------- Obteniendo conversacion tcp -------------------"
    pkts = []
    for pkt in captura:
        try:
            if pkt.transport_layer == 'TCP' and pkt.ip.src == IP_RED:
                pkts.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print "Error en tcp_conversartion_exchange"
    return pkts


def dist_remote_tcp_port(captura):  # N2
    """ Numero total de puertos distintos a los puertos TCP """
    print "--------------- Obteniendo dist remote tcp port -------------------"
    numero_puertos = 0
    for pkt in captura:
        try:
            if pkt.transport_layer == 'TCP' and pkt.ip.src == IP_RED:
                if pkt['TCP'].dstport != '80':
                    numero_puertos = numero_puertos + 1
        except AttributeError:
            pass
        except Exception, e:
            print 'Error en dist_remote_tcp_port'
            print e
    return numero_puertos

def remote_ips(pkts):  # N3
    """ Numero distinto de direcciones IP conectadas al emulador """
    print "--------------- Obteniendo remote ips -------------------"
    numero_ips = []
    for pkt in pkts:
        try:
            if pkt.ip.src == IP_RED:
                dst_addr = pkt.ip.dst
                if dst_addr != IP_RED:
                    if dst_addr not in numero_ips:
                        numero_ips.append(dst_addr)
        except AttributeError:
            pass
        except Exception:
            print 'Error en remote_ips'
    return numero_ips


def app_bytes(pkts):  # N4
    """ Numero de bytes de la capa de aplicacion que es enviado por el emulador
    hacia algun web, no se incluyen los datos de los servidores DNS """
    print "--------------- Obteniendo app bytes -------------------"
    tamanio_pkt = 0
    for pkt in pkts:
        try:
            tamanio_pkt = tamanio_pkt + int(pkt.captured_length)
        except AttributeError:
            pass
        except Exception:
            print 'Error en app_bytes'
    return tamanio_pkt

def source_app_packets(captura):  # N5
    """ Numero de paquetes enviados por la aplicación hacia el servidores remotos """
    print "--------------- Obteniendo source app pkts -------------------"
    pkts = []
    for pkt in captura:
        try:
            if pkt.ip.src == IP_RED:
                pkts.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print 'Error en source_app_packets'
    return pkts


def udp_packets(pkts):  # N6
    """ Numero de paquetes UDP, no se incluyen los datos de los DNS """
    print "--------------- Obteniendo udp pkt -------------------"
    pkts_temp = []
    for pkt in pkts:
        try:
            if pkt.ip.src == IP_RED:
                for lyr in pkt.layers:
                    if lyr.layer_name in 'udp':
                        if pkt not in pkts_temp:
                            pkts_temp.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print 'Error en udp_packets'
    return pkts_temp

def remote_app_packets(captura):  # N7
    """ Numero de paquetes enviados por el servidor remoto hacia la aplicación """
    print "--------------- Obteniendo remote pkts -------------------"
    pkts = []
    for pkt in captura:
        try:
            if pkt.ip.dst == IP_RED:
                pkts.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print 'Error en remote_app_packets'
    return pkts


def source_app_bytes(captura):  # N8
    """ volumen en bytes originados por la comunicación de la aplicación """
    print "--------------- Obteniendo src app bytes -------------------"
    tamanio_pkt = 0
    for pkt in captura:
        try:
            if pkt.ip.dst == IP_RED:
                tamanio_pkt = tamanio_pkt + int(pkt.captured_length)
        except AttributeError:
            pass
        except Exception:
            print 'Error en source_app_bytes'
    return tamanio_pkt


def remote_app_bytes(captura):  # N9
    """ volumen en bytes recibidos por la aplicación"""
    print "--------------- Obteniendo remote app bytes -------------------"
    tamanio_pkt = 0
    for pkt in captura:
        try:
            if pkt.ip.src == IP_RED:
                tamanio_pkt = tamanio_pkt + int(pkt.captured_length)
        except AttributeError:
            pass
        except Exception:
            print 'Error en remote_app_bytes'
    return tamanio_pkt

def http_pks(captura):  # N10
    """ Cantidad de paquetes http en la comunicación de la aplicación """
    print "--------------- Obteniendo paquetes HTTP -------------------"
    pkts = []
    for pkt in captura:
			if pkt[pkt.highest_layer].layer_name=="http":
		            if pkt.ip.src == IP_RED:
		                    pkts.append(pkt)

		  
    return pkts		
   

def app_packets(captura):  # N11
    """ numero de paquetes IP incluidos los del servidor DNS """
    print "--------------- Obteniendo app pkts -------------------"
    pkts_temp = []
    for pkt in captura:
        try:
            if pkt.ip.src == IP_RED:
                for lyr in pkt.layers:
                    if lyr.layer_name in 'ip':
                        if pkt not in pkts_temp:
                            pkts_temp.append(pkt)
        except AttributeError:
            pass
        except Exception:
            print 'Error en app_packets'
    return pkts_temp


def dns_query_times(captura): # N12
	""" Numero de paquetes DNS """
	print "--------------- Obteniendo DNS -------------------"
	pkts = []
	for pkt in captura:
			if pkt[pkt.highest_layer].layer_name=="dns":
		    		if pkt.dns.qry_name:
		    				if pkt.ip.src == IP_RED:
		    					pkts.append(pkt)

		  
	return pkts		
    	
def tipo(str):
    arrstr = str.split('/')
    return arrstr[2]


def nom(str):
    arrstr = str.split('/')
    return arrstr[3]

#for pk in cap:

#	cantidad=cantidad+app_bytes_p(pk)
	
#print "Metodo propio: " + str(cantidad)


def crear_matriz(ruta_datos, ruta_mtx_trans):
    """ Crea una matriz con las caracteristicas de la capa de transporte
    @param ruta_dataset ruta de los dataset a analizar
    @param ruta_matriz ruta del archivo a crear con la matriz de caracteristicas"""
    with open(name=ruta_problems_file, mode='w') as problems_txt:
        with open(name=ruta_mtx_trans, mode='w') as matriz:
            try:
                # id_url = linea.split(';')[0]
                # url = linea.split(';')[1]
                # cambiar a ip_honeypot a ip_android
                # IP_HONEYPOT = linea.split(';')[2]
               
                
                route = ''
                captura = pyshark.FileCapture

                # primero en el filecapture el pcap
                # luego ver como pyshark lee cada paquete y obtener el primero
                # con el primer paquete ver la ip src entonces esta va a ser el ip_honeypot
                # captura[0].ip.src
                print 'Extrayendo'
                f = open("routes.txt", "r")
                
                print route
                for g in f.readlines():
                    x=g.strip()

                    captura = pyshark.FileCapture(x)
                    #if len(captura) > 0:
                    try:
                            print "################### ESCRIBIENDO DATOS #############################"
                            print x
                            print "###################################################################"

                            pktss=pkt_without_dns(captura)
                            matriz.writelines(x + ';' + str(len(tcp_conversation_exchange(captura))) + ';'
                                              + str(dist_remote_tcp_port(captura)) + ';'
                                              + str(
                                len(remote_ips(pktss))) + ';'
                                              + str(app_bytes(pktss)) + ';'
                                              + str(
                                len(udp_packets(pktss))) + ';'
                                              + str(len(source_app_packets(captura))) + ';'
                                              + str(len(remote_app_packets(captura))) + ';'
                                              + str(source_app_bytes(captura)) + ';'
                                              + str(remote_app_bytes(captura)) + ';'
                                              + str(len(http_pks(captura))) + ';'
                                              + str(len(app_packets(captura))) + ';'
                                              + str(len(dns_query_times(captura))) + ';'  + '\n')
                    except Exception, e:
                            print "exception during the pcap lecture process"
                            print e
                            problems_txt.writelines(x + '\n')
                            captura.close()
                            break
                        	
                captura.close()
            except Exception, e:
                traceback.print_exc()


ruta_dataset = 'malware.csv'
ruta_matriz = 'general.csv'
ruta_problems_file = 'problems13.txt'
crear_matriz(ruta_dataset, ruta_matriz)
