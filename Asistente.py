import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request 
import json
import datetime
import wikipedia
import pyjokes
from time import time

#Tiempo de ejecución del programa
start_time = time()

#Ejecutar sentencias por medio de la voz
engine = pyttsx3.init()

#Nombre del asistente
name = 'alexa'

listener = sr.Recognizer()

#Colores
green_color = "\033[1;32;40m"
red_color = "\033[1;31;40m"
normal_color = "\033[0;37;40m"

#API Key
key = 'AIzaSyBXkyE9nb6GPIyJemIDYVGvsKX_3UYOH0U'

#Configuración de voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Método para que el asistente hable
def talk(text):
    engine.say(text)
    engine.runAndWait()

#Método para que el asistente escuche
def get_audio():
    r = sr.Recognizer()
    status = False

    with sr.Microphone() as source:
        print(f"{green_color} Escuchando...{normal_color}")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        rec = ""

        try:
            rec = r.recognize_google(audio, language='es-ES').lower()
            
            if name in rec:
                rec = rec.replace(f"{name} ", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                status = True
            else:
                print(f"Vuelve a intentarlo, no reconozco: {rec}")
        except:
            pass
    return {'text':rec, 'status':status}

#Método para que el asistente responda
while True:
    rec_json = get_audio()

    rec = rec_json['text']
    status = rec_json['status']

    if status:
        if 'estas ahi' in rec:
            talk('Por supuesto')
        
        elif 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            talk('Reproduciendo ' + music)
            pywhatkit.playonyt(music)
            
        elif 'cuantos suscriptores tiene' in rec:
            name_subs = rec.replace('cuantos suscriptores tiene', '')
            data = urllib.request.urlopen('https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername=' + name_subs.strip() + '&key=' + key).read()
            subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            talk(name_subs + " tiene {:,d}".format(int(subs)) + " suscriptores!")
            
        elif 'hora' in rec:
            hora = datetime.datetime.now().strftime('%I %M %p')
            talk("Son las "+hora)
        
        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            talk(info)
            
        elif 'chiste' in rec:
            chiste = pyjokes.get_joke("es")
            talk(chiste)
        
        elif 'descansa' in rec:
            talk("Saliendo...")
            break
        
        else:
            print(f"Vuelve a intentarlo, no reconozco: {rec}")
    
        
print(f"Vuelve a intentarlo, no reconozco: {rec}")