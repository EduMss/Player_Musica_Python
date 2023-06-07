import PySimpleGUI as pg
from pygame import mixer
import time

mixer.init()
tamanho = mixer.Sound('musica.mp3')
tamanhoSeg = tamanho.get_length()

tamanhoMin = int(tamanhoSeg / 60)
tamanhoSeg = int(tamanhoSeg - (tamanhoMin * 60))

mixer.music.load('musica.mp3')
mixer.music.play()
mixer.music.set_volume(0.01)#Setar o volume da musica entre 1.0 - 0.0 
mixer.music.get_volume()#pegar o volume que esta a musica
mixer.music.get_pos()#Mostrar o tempo que a musica ta em milissegundos
mixer.music.set_pos(2)

print(f"Minutos:{tamanhoMin}/Segundos:{tamanhoSeg}")

def TempoPecorrido():
    TempoPecorridoSeg = int(mixer.music.get_pos()/1000)
    TempoPecorridoMin = int(TempoPecorridoSeg / 60)
    TempoPecorridoSeg = int(TempoPecorridoSeg - (TempoPecorridoMin * 60))
    temp = '{:01d}:{:02d}'.format(TempoPecorridoMin,TempoPecorridoSeg)
    return temp

encerrar = True
while encerrar:
    print(TempoPecorrido())
    if mixer.music.set_endevent():
        # print("Ola")
        encerrar = False

