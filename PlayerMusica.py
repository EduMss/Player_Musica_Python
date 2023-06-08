import PySimpleGUI as sg
from pygame import mixer
import os

def Assets():
    Diretorio = os.path.join(os.path.dirname(__file__),"Assets")
    ListAssetsDir = {
        "icone":os.path.join(Diretorio, "musica.ico"),
        "fundo":os.path.join(Diretorio, "musica.png"),
        "pasta":os.path.join(Diretorio, "pasta-aberta-min.png"),
        "musica":os.path.join(Diretorio, "reprodutor-de-musica.png"),
        "play":os.path.join(Diretorio, "play.png"),
        "playlist":os.path.join(Diretorio, "playlist.png"),
    }
    return ListAssetsDir

ListAssetsDir = Assets()

class PlayMusica():
    def __init__(self, NomeMusica, CaminhoMusica, VolumeInicial = 0.05, PlayList = [], DiretorioPlayList = None):
        self.NomeMusica = NomeMusica
        self.CaminhoMusica = CaminhoMusica
        self.VolumeAtual = VolumeInicial
        self.PlayList = PlayList
        self.DiretorioPlayList = DiretorioPlayList
        self.IndexPlayList = 0


        layout = [
            [sg.Slider(key="Temporizador", size=(0, 10), range=(0, 1),enable_events=True, resolution=1, disable_number_display=True, orientation="h")],
            [sg.Text("Nome", key="NomeMusica")],
            [sg.Text("0:00", key="Tempo"),
             sg.Button('Anterior',key='Anterior'),
             sg.Button('Pausar',key='Pausar'),
             sg.Button('Proximo',key='Proximo'),
             sg.Button('Mutar', key="Mutar"),
             sg.Slider(key="Volume", range=(0, 1), resolution=0.01, enable_events=True, disable_number_display=True, orientation="h"),
             sg.Text("80%", key="VolumeTexto")
             ]
        ]

        self.window = sg.Window("Player Musica", layout=layout, element_justification='center', finalize=True, resizable=True, icon=ListAssetsDir['icone'])
        self.window['Temporizador'].expand(True, False, False)

    def IniciandoMusicaPlayList(self):
        mixer.init()
        mixer.music.load(self.CaminhoMusica)
        mixer.music.play()
        self.TimeMusica = 0

    def IniciandoMusica(self,IndiceMusica = -1):
        if IndiceMusica == -1:
            mixer.init()
            mixer.music.load(self.CaminhoMusica)
            mixer.music.play()
            self.TimeMusica = 0
        else:
            mixer.init()
            self.IndexPlayList = IndiceMusica
            self.CaminhoMusica = os.path.join(self.DiretorioPlayList,self.PlayList[IndiceMusica])
            self.NomeMusica = self.PlayList[IndiceMusica]
            mixer.music.load(self.CaminhoMusica)
            mixer.music.play()
            self.TimeMusica = 0
            self.AlterarInfoMusicaInicial()

    def AlterarVolume(self, Volume):
        mixer.music.set_volume(Volume)
        self.window['VolumeTexto'].update(f'{int(Volume * 100)}%')

    def AlterarInfoMusicaInicial(self):
        # mudando o nome da musica
        self.window['NomeMusica'].update(self.NomeMusica)

        # Inserindo o tempo total da musica
        self.tamanho = mixer.Sound(self.CaminhoMusica)
        self.tamanho = self.tamanho.get_length()
        tamanhoMin = int(self.tamanho / 60)
        tamanhoSeg = int(self.tamanho - (tamanhoMin * 60))
        self.tamanhoMusica = '{:01d}:{:02d}'.format(tamanhoMin,tamanhoSeg)
        self.window['Tempo'].update(f'0:00/{self.tamanhoMusica}')

        # aumentando o range do Slider(Temporizador) da musica para q eu consega mover segundo por segundo
        self.window['Temporizador'].update(range=(0,int(self.tamanho)))

        # alterar as informações do volume
        self.window['Volume'].update(self.VolumeAtual)
        self.AlterarVolume(self.VolumeAtual)

    def Mutar(self, VolumeAtual):
        if mixer.music.get_volume() == 0:
            self.AlterarVolume(self.VolumeAtual)
            self.window['Volume'].update(self.VolumeAtual)
        else :
            self.VolumeAtual = VolumeAtual
            self.AlterarVolume(0)
            self.window['Volume'].update(0)

    def AlterarInfoMusica(self):
        self.TempoPecorridoTotal = int(int(mixer.music.get_pos()/1000) + self.TimeMusica)
        TempoPecorridoMin = int(self.TempoPecorridoTotal / 60)
        TempoPecorridoSeg = int(self.TempoPecorridoTotal - (TempoPecorridoMin * 60))
        TempoPecorrido = '{:01d}:{:02d}'.format(TempoPecorridoMin,TempoPecorridoSeg)
        self.window['Tempo'].update(f'{TempoPecorrido}/{self.tamanhoMusica}')

        self.window['Temporizador'].update(int(int(mixer.music.get_pos()/1000) + self.TimeMusica))

    def Pause(self):
        if mixer.music.get_busy():
            self.IsPause = True
            mixer.music.pause()
            self.window['Pausar'].update("Play")
        else :
            self.IsPause = False
            mixer.music.unpause()
            self.window['Pausar'].update("Pause")

    def MudarPosicaoMusica(self,NovaPosicao):
        mixer.music.play(0, NovaPosicao)
        self.TimeMusica = NovaPosicao

        TempoPecorridoSeg = NovaPosicao
        TempoPecorridoMin = int(TempoPecorridoSeg / 60)
        TempoPecorridoSeg = int(TempoPecorridoSeg - (TempoPecorridoMin * 60))
        TempoPecorrido = '{:01d}:{:02d}'.format(TempoPecorridoMin,TempoPecorridoSeg)
        self.window['Tempo'].update(f'{TempoPecorrido}/{self.tamanhoMusica}')

    def func(self):
        rodando = True
        self.IniciandoMusica()
        self.AlterarInfoMusicaInicial()
        
        while rodando:
            self.event, self.value = self.window.read(timeout=1000)

            if self.event == sg.WIN_CLOSED:
                self.window.close()
                rodando = False
                break

            elif self.event == 'Volume':
                self.AlterarVolume(self.value['Volume'])

            elif self.event == 'Pausar':
                self.Pause()

            elif self.event == 'Mutar':
                self.Mutar(self.value['Volume'])

            elif self.event == 'Temporizador':
                self.MudarPosicaoMusica(self.value['Temporizador'])
                

            elif self.event == 'Anterior':
                if self.DiretorioPlayList == None:
                    self.IniciandoMusica()
                else:
                    if self.IndexPlayList - 1 < 0 :
                        self.IniciandoMusica(len(self.PlayList)-1)
                    else:
                        self.IniciandoMusica(self.IndexPlayList-1)
            elif self.event == 'Proximo':
                if self.DiretorioPlayList == None:
                    self.IniciandoMusica()
                else:
                    if self.IndexPlayList >= len(self.PlayList)-1 :
                        self.IniciandoMusica(0)
                    else:
                        self.IniciandoMusica(self.IndexPlayList+1)

            elif mixer.music.get_busy() == False and self.IsPause == False:
                if self.DiretorioPlayList == None:
                    self.IniciandoMusica()
                else:
                    if self.IndexPlayList >= len(self.PlayList)-1 :
                        self.IniciandoMusica(0)
                    else:
                        self.IniciandoMusica(self.IndexPlayList+1)

            

            self.AlterarInfoMusica()
            

class TelaInicial():
    def __init__(self):
        layout = [
            [sg.Button(image_filename=ListAssetsDir['musica'], image_size=(45,45), key="BrowsePlay"),sg.Button(image_filename=ListAssetsDir['pasta'], image_size=(45,45), key="BrowsePlayList")],
            [sg.Listbox(key='ArquivosList', values=[], size=(0,5), font=('Arial',20), default_values=0)],
            [sg.Button(image_filename=ListAssetsDir['play'], key='AbrirArquivo'), sg.Button(image_filename=ListAssetsDir['playlist'], key='AbrirPlayList')]
        ]

        self.window = sg.Window("Player De Musica", layout=layout, element_justification='center', finalize=True, resizable=True, icon=ListAssetsDir['icone'])
        self.window['ArquivosList'].expand(True,True,True)
        self.window['AbrirArquivo'].expand(True,False,False)
        self.window['AbrirPlayList'].expand(True,False,False)
        self.window['BrowsePlay'].expand(True,False,False)
        self.window['BrowsePlayList'].expand(True,False,False)

    def ProcurarMusicas(self, pasta = None):
        self.FormatosAceitos = [".mp3", ".MP3", ".WMA"]
        self.ListaMusicas = []
        if pasta == None or pasta == "":
            for file in os.listdir(os.path.dirname(__file__)):
                for formato in self.FormatosAceitos:
                    if file.endswith(formato):
                        self.ListaMusicas.append(file)
            self.CaminhoMusica = os.path.join(os.path.dirname(__file__))
            self.window['ArquivosList'].update(self.ListaMusicas)
        else:
            for file in os.listdir(pasta):
                for formato in self.FormatosAceitos:
                    if file.endswith(formato):
                        self.ListaMusicas.append(file)
            self.CaminhoMusica = os.path.join(pasta)
            self.window['ArquivosList'].update(self.ListaMusicas)

    def func(self):
        self.ProcurarMusicas()
        rodando = True
        Abrir = ""
        while rodando:
            self.event, self.value = self.window.read(timeout=1000)

            if self.event == sg.WIN_CLOSED:
                rodando = False
                self.window.close()

            elif self.event == "AbrirArquivo":
                Musica = str(self.window['ArquivosList'].get())

                ListaCaracteresRemover = ('[',']',"'")
                for Caracter in ListaCaracteresRemover:
                    index = ListaCaracteresRemover.index(Caracter)
                    if ListaCaracteresRemover[index] in Musica:
                        Musica = Musica.replace(ListaCaracteresRemover[index], '')

                self.CaminhoMusica = os.path.join(self.CaminhoMusica, Musica)
                Abrir = "Player"
                rodando = False
                self.window.close()

            elif self.event == "BrowsePlay":
                file = sg.popup_get_file('', multiple_files=False, no_window=True)
                for formato in self.FormatosAceitos:
                    if file.endswith(formato):
                        if (file.find("/")):
                            pos = file.rfind("/")
                            NomeMusica = file[pos+1:]
                            print("tem / : "+NomeMusica)
                        elif (file.find("\\")):
                            pos = file.find("\\")
                            NomeMusica = file[pos+1:]
                            print("tem \\ : "+NomeMusica)
                        PlayMusica(NomeMusica = NomeMusica, CaminhoMusica = file).func()
                        rodando = False
                        self.window.close()
                

            elif self.event == "BrowsePlayList":
                NovaPasta = sg.popup_get_folder('', no_window=True)
                self.ProcurarMusicas(NovaPasta)

            elif self.event == "AbrirPlayList":
                self.DiretorioPlayList = self.CaminhoMusica
                self.PlayList = self.ListaMusicas
                Abrir = "AbrirPlayList"

                Musica = str(self.window['ArquivosList'].get())
                if len(self.window['ArquivosList'].get()) == 0:
                    Musica = self.ListaMusicas[0]

                ListaCaracteresRemover = ('[',']',"'")
                for Caracter in ListaCaracteresRemover:
                    index = ListaCaracteresRemover.index(Caracter)
                    if ListaCaracteresRemover[index] in Musica:
                        Musica = Musica.replace(ListaCaracteresRemover[index], '')
                self.CaminhoMusica = os.path.join(self.CaminhoMusica, Musica)
                rodando = False
                self.window.close()

        if Abrir == "Player":
            PlayMusica(NomeMusica = Musica, CaminhoMusica = self.CaminhoMusica).func()
        elif Abrir == "AbrirPlayList":
            PlayMusica(NomeMusica = Musica, CaminhoMusica = self.CaminhoMusica, PlayList = self.PlayList, DiretorioPlayList = self.DiretorioPlayList).func()

TelaInicial().func()