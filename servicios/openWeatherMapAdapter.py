import urllib2, json 

from datetime import datetime, timedelta

class OpenWeatherMapAdapter:

    appid = "713d008f823124ef813cfef342341934"
    cache = {}
    cielo_traductor = {"clouds":"Nublado","clear":"Despejado", "rain":"Lluvias"}
    descripcion_traductor = { 
                             "sky is clear":"Cielo despejado, dia soleado", 
                             "light rain":"Lluvias moderadas",
                             "few clouds": "Pocas nubes",
                             "scattered clouds": "Nubes espesas",
                             "overcast clouds": "Nubes de tormenta",
                             "broken clouds":"Nubes de tormenta",
                             "shower rain": "Lluvias copiosas",
                             "rain": "Lluvias de moderadas a fuertes",
                             "thunderstorm": "Tormentas de rayos",
                             "snow": "Se esperan nevadas",
                             "mist": "Probabilidad de neblina"
              
                             }
    def caduco_valor_en_cache(self,fecha):
        delta = datetime.now() - fecha
        days, hours, minutes = delta.days, delta.seconds // 3600, delta.seconds // 60 % 60
        return (days>1 or hours>8)

    def obtener_clima(self,nombre_ciudad):
        if nombre_ciudad in self.cache and not self.caduco_valor_en_cache(self.cache[nombre_ciudad]["fecha"]):
            return self.cache[nombre_ciudad]["resultado"]
        else:
            resultado = self.hacer_request(nombre_ciudad)
            resultado_cacheado = {"fecha": datetime.now(),"resultado": resultado}
            self.cache[nombre_ciudad] = resultado_cacheado
            return resultado

    def hacer_request(self,nombre_ciudad):
        url = "http://api.openweathermap.org/data/2.5/weather?q="+nombre_ciudad+"&units=metric"+"&appid="+ self.appid

        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        resultado = json.loads(response.read())
        return resultado

    def get_clima(self,nombre_ciudad):

        resultado=self.obtener_clima(nombre_ciudad)
        clima = {
            'ubicacion': nombre_ciudad,
            'cielo': self.cielo_traductor[resultado["weather"][0]["main"].lower()],
            'descripcion': self.descripcion_traductor[resultado["weather"][0]["description"].lower()],
            'temperatura': resultado["main"]["temp"],
            'icono' : resultado["weather"][0]["icon"]
        }
        return clima
