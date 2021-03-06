import shodan


class Info_Shodan():
    def __init__(self):

        self.key = open('apikey-shdn.txt').readline().rstrip('\n')
        self.api = shodan.Shodan(self.key)
        self.resultado_total = None
        self.resultado_matches = None
        self.array_ip = []

    def buscar(self,busqueda,nlimit=10):
        try:
            resultados = self.api.search(busqueda,limit=nlimit)
            #resultados = self.api.search('proconsi',limit=15)
            print("Resultados totales: "+str(resultados['total']))
            print("Fin de la Búsqueda")

            self.resultado_total = resultados['total']
            self.nlimit = nlimit

            if(self.resultado_total < self.nlimit):
                self.nlimit = self.resultado_total

            if self.resultado_total == 0:
                return False

            self.resultado_matches = resultados['matches']
            return True

        except shodan.APIError as e:
            print('Error ishodan: %s' % e)
            return('Error ishodan: %s' % e)

    def host(self,ip):
        cadena="\n<b>**INFORMACIÓN DEL HOST**</b>\n\n"
        host = self.api.host(ip)
        print(host)

        for c,item in enumerate(host["data"]):
            print(str(c)+" OTRO ... \n")
            print(item["opts"])
            print()

        cadena+='<b>IP:</b> {}\n'.format(host['ip_str'])
        cadena+='<b>Organizacion:</b> {}\n'.format(host.get('org', 'n/a'))
        cadena+='<b>Sistema operativo:</b> {}\n'.format(host.get('os', 'n/a'))
        cadena+='<b>Ciudad:</b> {}\n'.format(host.get('city', 'n/a'))
        cadena+='<b>Codigo region:</b> {}\n'.format(host.get('region_code', 'n/a'))
        cadena+='<b>Codigo area:</b> {}\n'.format(host.get('area_code', 'n/a'))
        cadena+='<b>Ultima actualizacion:</b> {}\n'.format(host.get('last_update', 'n/a'))
        cadena+='<b>Codigo pais:</b> {}\n'.format(host.get('country_code3', 'n/a'))
        cadena+='<b>Nombre pais:</b> {}\n'.format(host.get('country_name', 'n/a'))
        cadena+='<b>Latitud:</b> {}\n'.format(host.get('latitude', 'n/a'))
        self.lat = host.get('latitude', 'n/a')
        cadena+='<b>Longitud:</b> {}\n'.format(host.get('longitude', 'n/a'))
        self.log = host.get('longitude', 'n/a')
        cadena+='<b>Isp:</b> {}\n'.format(host.get('isp', 'n/a'))
        cadena+='<b>Asn:</b> {}\n'.format(host.get('asn', 'n/a'))
        cadena+='<b>Hostname:</b> {}\n'.format(host.get('hostname', 'n/a'))
        cadena+='<b>Puertos:</b> {}\n'.format(host.get('ports', 'n/a'))
        print()
        cadena+="\n\n<b>Información de puertos:</b>\n\n"

        for dato in host['data']:
            cadena+="<b>Puerto:</b> {}\n".format(dato['port'])
            cadena+="<b>Transporte:</b> {}\n".format(dato['transport'])
            cadena+="<b>Banner:</b> {}\n".format(dato['data'])

        for dato in host['data']:
            print ('Puerto: %s ' % dato['port'])
            print ('Transport: %s ' % dato['transport'])
            print ('Banner: %s ' % dato['data'])

        return cadena

    def localizacion(self):
        if(self.lat==None or self.log==None):
            return False
        else:
            return str(self.lat)+";"+str(self.log)

    def datos_telegram_location(self,location):
        texto = "\n"
        log = 0.0
        lat = 0.0
        texto+="<strong>Localizacion</strong>: \n"
        if(location['city'] != None):
            texto+="\t\t\t<strong>Ciudad</strong>: "+str(location['city'])+"\n"

        if(location['country_code'] != None):
            texto+="\t\t\t<strong>Codigo pais</strong>: "+str(location['country_code'])+"\n"

        if(location['country_name'] != None):
            texto+="\t\t\t<strong>Nombre pais</strong>: "+str(location['country_name'])+"\n"

        if(location['area_code'] != None):
            texto+="\t\t\t<strong>Codigo area</strong>: "+str(location['area_code'])+"\n"

        if(location['longitude'] != None):
            texto+="\t\t\t<strong>longitud</strong>: "+str(location['longitude'])+"\n"

        if(location['latitude'] != None):
            texto+="\t\t\t<strong>latitud</strong>: "+str(location['latitude'])+"\n"

        if(location['postal_code'] != None):
            texto+="\t\t\t<strong>Codigo postal</strong>: "+str(location['postal_code'])+"\n"

        texto+= "\n"
        return texto

    def obtener_token_array_ip(self):
        token = ""
        n = len(self.array_ip)-1
        for index,clave in enumerate(self.array_ip):
            if(index == n):
                token+=str(clave[0])+"="+str(clave[1])
            else:
                token+=str(clave[0])+"="+str(clave[1])+","
        return token;

    def datos_telegram(self):
        mi_array = []
        
        self.diccionario_ip = {}

        cont = 1
        for i in self.resultado_matches:
            texto = "<strong>"+str(cont)+")</strong>\n\n"
            ip = i['ip_str']
            texto+=("<strong>IP:</strong> %s\n" % ip)

            array_ip_cont = [cont,ip]
            self.array_ip.append(array_ip_cont)

            #texto+=("<strong>Modulo:</strong> %s\n" % i['module'])
            texto+=("<strong>ISP:</strong> %s\n" % i['isp'])

            texto+=("<strong>Hostnames:</strong> %s\n" % i['hostnames'])
            texto+=("<strong>Puerto:</strong> %s\n" % i['port'])

            texto+=self.datos_telegram_location(i['location'])

            data = i['data']
            n_data_len = len(data)
            if(n_data_len >= 40):
                data = data[0:45]
            #print("logitud: ",len(data))
            #exit()
            texto+=("<strong>Datos:</strong><code>\n%s\n</code>" % data)
            texto+=('')
            cont=cont+1
            #print(i)
            #exit()
            mi_array.append(texto)
        return mi_array

if __name__ == "__main__":
    print("Ejemplo")
    i = Info_Shodan()
    #res = i.host("41.142.245.134")
    res = i.host("196.41.217.237")
    #if(res==True):
    #    print(i.datos_telegram())
    #else:
    #    print(res)
